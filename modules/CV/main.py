import cv2
import dlib
from imutils import face_utils
import time
import os
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service


class CV:
    def __init__(self):
        self.path = os.getcwd()
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(f"{self.path}/modules/shape_predictor_68_face_landmarks.dat")
        self.state = True
        self.driver = None
        self.__data = ""
        self._setup_browser()

    def _setup_browser(self):
        """Настройка Яндекс.Браузера через Selenium"""
        options = Options()

        # Путь к Яндекс.Браузеру
        options.binary_location = r'C:\Users\79826\AppData\Local\Yandex\YandexBrowser\Application\browser.exe'

        # Настройки для автоматизации
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')

        service = Service(
            executable_path=r'C:\Users\79826\Desktop\VKR\desktop\yandexdriver.exe'  # Укажите правильный путь
        )

        self.driver = webdriver.Chrome(
            service=service,    # Передаем service вместо executable_path
            options=options
        )

    def get_data(self):
        return self.__data

    def get_image(self):
        """Основной метод для захвата и анализа изображения"""
        try:
            self.driver.get('https://telemost.yandex.ru/j/30527821286466')
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, 'video'))
            )

            while self.state:
                self.process_page()
                time.sleep(1)  # Пауза между итерациями

        except Exception as e:
            print(f"Ошибка браузера: {e}")
        finally:
            self.cleanup()

    def process_page(self):
        """Обработка элементов страницы"""
        videos = self.driver.find_elements(By.TAG_NAME, 'video')
        names = self.driver.find_elements(By.CSS_SELECTOR, 'span.TextName_BOaIg')

        for video, name in zip(videos, names):
            user = name.text
            self.process_video(video, user)

    def change_state(self, state: bool):
        self.state = state

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

    def process_video(self, video, user):
        """Обработка видео элемента"""
        try:
            # Получаем скриншот элемента
            screenshot = video.screenshot_as_png
            img = cv2.imdecode(
                np.frombuffer(screenshot, np.uint8), 
                cv2.IMREAD_COLOR
            )

            # Анализ изображения
            self.analyze_frame(img, user)

        except Exception as e:
            print(f"Ошибка обработки видео: {e}")

    def analyze_frame(self, frame, user):
        """Анализ кадра"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)

        if faces:
            for face in faces:
                landmarks = self.predictor(gray, face)
                landmarks = face_utils.shape_to_np(landmarks)
                gaze_ratio = self.calculate_gaze_ratio(landmarks)[0]
                self.__data += f"{user} ; {gaze_ratio} ; Нейтрально || "

    def cleanup(self):
        """Корректное завершение работы"""
        if self.driver:
            self.driver.quit()

    def stop(self):
        """Остановка"""
        self.state = False
        self.cleanup()


# if __name__ == "__main__":
#     analyzer = CV()
#     try:
#         analyzer.get_image()
#     except KeyboardInterrupt:
#         analyzer.stop()