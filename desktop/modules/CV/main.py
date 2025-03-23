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
from random import randint


# Инициализация детектора лиц и предиктора ключевых точек
path = str(os.getcwd())
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(f"{path}/modules/shape_predictor_68_face_landmarks.dat")
data_from_video = ""
start_recognize = time.time()
mark = "0"
stop_thread = False


def timer() -> str:
    """Возврат времени записи"""
    return str(timedelta(seconds=time.time() - start_recognize))


def get_mark(text_: str = None) -> str:
    """Возвращаем оценку"""
    for i in range(0, 1000):
        i = i + 1
    return str(randint(0, 100))


def change_state(state: bool = False) -> None:
    global stop_thread
    stop_thread = state
    return None


def get_mark_v() -> str:
    global mark
    return mark


def show_information_from_data():
    global data_from_video
    global mark

    print("::Начинаем вычислять оценку::")
    with ThreadPoolExecutor() as executor:
        future = executor.submit(get_mark, data_from_video)
        mark = future.result()
        print("::Оценка получена::")
    print("::Обнуляем данные::")
    data_from_video = ""


def calculate_gaze_ratio(landmarks: np.ndarray = None):
    left_eye = []
    right_eye = []

    for n in range(36, 42):  # Левый глаз
        x = landmarks[n][0]
        y = landmarks[n][1]
        left_eye.append((x, y))
    for n in range(42, 48):  # Правый глаз
        x = landmarks[n][0]
        y = landmarks[n][1]
        right_eye.append((x, y))

    left_eye_center = np.mean(left_eye, axis=0).astype(int)
    right_eye_center = np.mean(right_eye, axis=0).astype(int)

    nose_tip = landmarks[30]  # Нос

    gaze_vector_left = np.array([left_eye_center[0] - nose_tip[0], left_eye_center[1] - nose_tip[1]])
    gaze_vector_right = np.array([right_eye_center[0] - nose_tip[0], right_eye_center[1] - nose_tip[1]])

    gaze_vector_left = gaze_vector_left / np.linalg.norm(gaze_vector_left)
    gaze_vector_right = gaze_vector_right / np.linalg.norm(gaze_vector_right)

    gaze_ratio_left = np.dot(gaze_vector_left, np.array([1, 0]))
    gaze_ratio_right = np.dot(gaze_vector_right, np.array([1, 0]))

    gaze_ratio = (gaze_ratio_left + gaze_ratio_right) / 2
    return gaze_ratio


def analyze_faces(gray, frame, faces):
    global data_from_video
    for i, face in enumerate(faces):
        landmarks = predictor(gray, face)
        landmarks = face_utils.shape_to_np(landmarks)

        # Определение эмоции
        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            emotion = result[0]['dominant_emotion']
        except Exception as e:
            emotion = "Unknown"

        # # Определение направления взгляда
        gaze_ratio = calculate_gaze_ratio(landmarks)
        looking_percentage = max(0, min(1, gaze_ratio)) * 100

        data_from_video += f"Время - {timer()}; Пользователь {i+1} смотрит на экран с точностью {looking_percentage:.2f}%. Эмоция: {emotion}\n"


def main():
    global stop_thread

    schedule.every(30).seconds.do(show_information_from_data)
    while stop_thread != True:
        schedule.run_pending()

        # Захват экрана
        screen = pyautogui.screenshot()
        frame = np.array(screen)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        if faces:
            analyze_faces(gray, frame, faces)


if __name__ == "__main__":
    main()