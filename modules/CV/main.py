import cv2
import dlib
from imutils import face_utils
from deepface import DeepFace
import pyautogui
import numpy as np
import os
from datetime import timedelta
import time
import schedule
from concurrent.futures import ThreadPoolExecutor
import requests


class Recoginze():
    path: str = os.getcwd()
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(f"{path}/modules/shape_predictor_68_face_landmarks.dat")

    def __init__(self):
        self.data_from_video = ''
        self.start_recognize = time.time()
        self.mark = '100'
        self.stop_thread = False
        self.id = 0
        self.lid = 0
        self.temp_ = '100'

    def __timer(self) -> str:
        return str(timedelta(seconds=time.time() - self.start_recognize))

    def mark_value(self) -> str:
        return self.temp_

    def analyz(self, text: str = None) -> str:
        if text == '':
            text = f'{self.__timer()} ; FaceNotFound'
        upload = requests.patch(url='http://127.0.0.1:8000/analyz/', json={'id': self.id, 'lid': self.lid, "audio": f'{self.__timer()} ; AudioNotFound\n', "video": text})
        mark = requests.get(url=f'http://127.0.0.1:8000/analyz/mark?id={str(self.id)}')

        if mark.text != '"No"':
            text = mark.text.removeprefix('"')
            text = text.removesuffix('"')
            self.mark = int(text)
            self.temp_ = self.mark
        else:
            self.mark = self.temp_

    def change_state(self, state: bool = False) -> None:
        self.stop_thread = state

    def get_analyz_data(self):
        print("::Начинаем вычислять оценку::")
        with ThreadPoolExecutor() as executor:
            future = executor.submit(self.analyz, self.data_from_video)
            self.mark = future.result()
            print("::Оценка получена::")
        print("::Обнуляем данные::")
        self.data_from_video = ""

    def calculate_gaze_ratio(self, landmarks: np.ndarray, calibration_data: dict = None):
        # Инициализация калибровочных данных при первом вызове
        if calibration_data is None:
            calibration_data = {
                'calibrated': False,
                'ref_eyes_distance': None,
                'ref_pupils': None,
                'threshold': 0.1
            }

        # Извлечение точек глаз
        left_eye = np.array([(landmarks[n][0], landmarks[n][1]) for n in range(36, 42)])
        right_eye = np.array([(landmarks[n][0], landmarks[n][1]) for n in range(42, 48)])
        
        # Вычисление характеристик глаз
        def eye_features(eye_points):
            pupil = np.mean(eye_points[1:5], axis=0)  # Положение зрачка
            center = np.mean(eye_points, axis=0)
            A = np.linalg.norm(eye_points[1] - eye_points[5])
            B = np.linalg.norm(eye_points[2] - eye_points[4])
            C = np.linalg.norm(eye_points[0] - eye_points[3])
            ear = (A + B) / (2.0 * C)  # Коэффициент открытости глаза
            return center, pupil, ear

        left_center, left_pupil, left_ear = eye_features(left_eye)
        right_center, right_pupil, right_ear = eye_features(right_eye)

        # Проверка открытости глаз
        if left_ear < 0.25 or right_ear < 0.25:
            return 0.0, calibration_data  # Глаза закрыты

        # Вычисление вектора между глазами
        eyes_vector = right_center - left_center
        eyes_distance = np.linalg.norm(eyes_vector)

        # Калибровка при первом вызове
        if not calibration_data['calibrated']:
            calibration_data['ref_eyes_distance'] = eyes_distance
            calibration_data['ref_pupils'] = (
                (left_pupil - left_center) / eyes_distance,
                (right_pupil - right_center) / eyes_distance
            )
            calibration_data['calibrated'] = True
            return 1.0, calibration_data  # Нейтральное значение при калибровке

        # Нормализованные координаты зрачков
        current_left = (left_pupil - left_center) / calibration_data['ref_eyes_distance']
        current_right = (right_pupil - right_center) / calibration_data['ref_eyes_distance']

        # Вычисление отклонений от калибровочных значений
        delta_left = np.linalg.norm(current_left - calibration_data['ref_pupils'][0])
        delta_right = np.linalg.norm(current_right - calibration_data['ref_pupils'][1])

        # Комбинированный результат (0.0 - не смотрит, 1.0 - смотрит)
        gaze_ratio = 1.0 - np.clip((delta_left + delta_right)/2, 0, calibration_data['threshold']*2)/calibration_data['threshold']

        return gaze_ratio, calibration_data

    def analyze_faces(self, gray, frame, faces):
        for i, face in enumerate(faces):
            landmarks = self.predictor(gray, face)
            landmarks = face_utils.shape_to_np(landmarks)

            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

            # # Определение направления взгляда
            gaze_ratio = self.calculate_gaze_ratio(landmarks)[0]

            self.data_from_video += f"{self.__timer()} ; {i} ; {gaze_ratio} ; Нейтрально\n"

    def main(self):
        schedule.every(60).seconds.do(self.get_analyz_data)
        while self.stop_thread is not True:
            schedule.run_pending()

            # Захват экрана
            screen = pyautogui.screenshot()
            frame = np.array(screen)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.detector(gray)

            if faces:
                self.analyze_faces(gray, frame, faces)
