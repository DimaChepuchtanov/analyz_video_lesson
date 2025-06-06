import tkinter as tk
from ctypes import windll
import sys
from threading import Thread, Event
from PIL import Image, ImageTk
from requests import post
import sys, os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from setting import setting
import requests
import schedule
from datetime import timedelta
import time
from random import randint
import asyncio


GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080


class Load(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Загрузка")

        # Центрирование окна
        self.center_window(600, 400)

        # Загрузка и отображение GIF
        self.load_gif("img\\load_gif.gif")  # Укажите путь к вашему GIF-файлу

        # Запуск анимации
        self.animate(0)

    def center_window(self, width, height):
        """Центрирует окно на экране"""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")

    def load_gif(self, filepath):
        """Загружает анимированный GIF"""
        try:
            self.gif = Image.open(filepath)
            self.frames = []

            # Извлекаем все кадры из GIF
            for frame in range(0, self.gif.n_frames):
                self.gif.seek(frame)
                frame_image = ImageTk.PhotoImage(self.gif.copy())
                self.frames.append(frame_image)

            # Создаем Label для отображения анимации
            self.label = tk.Label(self)
            self.label.pack(expand=True, fill='both')

        except Exception as e:
            print(f"Ошибка загрузки GIF: {e}")

    def animate(self, frame_num):
        """Обновляет анимацию"""
        if frame_num < len(self.frames):
            self.label.configure(image=self.frames[frame_num])
            self.after(self.gif.info['duration'], 
                        lambda: self.animate((frame_num + 1) % len(self.frames)))


class CustomWindow(tk.Tk):
    def __init__(self, cv, nlp):
        super().__init__()

        self.mark = '100'
        self.schedule_state = True
        # Удаление рамок и кнопок
        self.overrideredirect(True)

        # Установка атрибутов окна для отображения на панели задач
        self.wm_attributes("-topmost", True)  # Принудительное отображение на панели задач
        self.update_idletasks()  # Обновление состояния окна

        # Создание заголовка окна
        self.title_bar = tk.Frame(self, bg='grey', height=30)
        self.title_bar.pack(fill=tk.X)

        # Добавление метки заголовка
        self.title_label = tk.Label(self.title_bar, text="Rec", bg='grey', fg='white')
        self.title_label.pack(side=tk.LEFT, padx=5)

        # Добавление кнопки закрытия
        self.close_button = tk.Button(self.title_bar, text="X", command=self.close, bg='grey', fg='white', bd=0)
        self.close_button.pack(side=tk.RIGHT)

        # Добавление основного контента
        self.content_frame = tk.Frame(self, bg='white')
        tk.Frame(self, bg="white").pack(fill=tk.BOTH, expand=True)
        self.start_button = tk.Button(self.content_frame, text="Старт", bg='grey', fg='white', border=1, command=self.start)
        self.start_button.pack(fill=tk.BOTH, expand=True)
        tk.Button(self.content_frame, text="Стоп", bg='grey', fg='white', border=1, command=self.stop).pack(fill=tk.BOTH, expand=True)
        button_ = tk.Button(self.content_frame, text="Оценка", bg='grey', fg='white', border=1)
        button_.pack(fill=tk.BOTH, expand=True)
        but = tk.Button(self.content_frame, text="Подробнее", bg='grey', fg='white', border=1)
        but.pack(fill=tk.BOTH, expand=True)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        # Добавление функциональности перемещения окна
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<ButtonRelease-1>", self.stop_move)
        self.bind("<B1-Motion>", self.on_motion)

        # Привязка событий к кнопке
        button_.bind("<ButtonPress-1>", self.open_secondary_window)
        button_.bind("<ButtonRelease-1>", self.close_secondary_window)

        but.bind("<ButtonPress-1>", self.open_long_window)
        but.bind("<ButtonRelease-1>", self.close_long_window)

        self.x = self.y = 0
        self.after(10, lambda: self.set_appwindow())

        # Переменная для хранения ссылки на второе окно
        self.secondary_window = None
        self.secondar_window = None
        self.id_analyz, self.lesson_id = self.create_row()
        self.cv, self.nlp = cv, nlp
        self.id = self.id_analyz
        self.lid = self.lesson_id
        self.statistic = """0:00:30
Дима Чепуштанов - Взгляд на экран колеблется между отсутствием и полной концентрацией, эмоция нейтральная.
0:01:00
Дима Чепуштанов - Взгляд на экран часто фокусируется, но периодически отвлекается, эмоция нейтральная"""

    def __timer(self) -> str:
        return str(timedelta(seconds=time.time() - self.timer))

    def create_row(self) -> int:
        request_file = post(url='http://127.0.0.1:8000/file/', json={"path": "None",
                                                                     "duration": "00:00:00",
                                                                     "size": "0 bytes",
                                                                     "text_data": "None"})

        if request_file.status_code != 200:
            print('Erooor insert file')
            self.destroy()

        file_id = dict(eval(request_file.content))
        file_id = int(file_id['id'])

        uid = self.reload_user()
        request_lesson = post(url='http://127.0.0.1:8000/lesson/?token=Ymka', json={"uid": uid,
                                                                         "name": "string",
                                                                         "file": file_id})
        if request_lesson.status_code != 200:
            print('Erooor insert lesson')
            self.destroy()

        lesson_id = dict(eval(request_lesson.content))
        lesson_id = int(lesson_id['id'])

        result = post(url='http://127.0.0.1:8000/analyz/?token=Ymka', json={"lid": lesson_id,
                                                                 "audio": "Start",
                                                                 "video": "Start"})

        if result.status_code != 200:
            print('Erooor insert analyz')
            self.destroy()

        analyz_id = result.content
        analyz_id = int(analyz_id)
        return analyz_id, lesson_id

    def reload_user(self):
        config_data = setting.read_data_config()
        try:
            user_id = config_data.getint("user", "uid")
        except Exception:
            user_id = None
        try:
            return user_id
        except Exception:
            return user_id

    def schedules(self):
        while self.schedule_state:
            schedule.run_pending()

    def start(self):
        self.cv.change_state(state=True)
        self.nlp.change_state(state=True)

        self.start_button.config(state=tk.DISABLED)
        self.timer = time.time()
        Thread(name="recog_cv", target=self.cv.get_image, daemon=True).start()
        Thread(name="recog_nlp", target=self.nlp.main).start()
        schedule.every(30).seconds.do(self.analyz)
        Thread(name='schedule', target=self.schedules).start()

    def stop(self):
        self.cv.change_state(state=False)
        self.nlp.change_state(state=False)

        # self.start_button.config(state=tk.ACTIVE)
        schedule.cancel_job(schedule.get_jobs()[-1])
        self.schedule_state = False

        # TODO
        # Нужно сделать так, чтобы при нажатии на закрыть, приложение открывало главное меню
        # Тут, при нажатии на стоп, все данные, которые необходимо, переходили в таблицу Урока

    def close(self):
        self.destroy()
        # subprocess.Popen(['python', 'app.py'])
        sys.exit()

    def analyz(self):
        cv_data = self.cv.get_data()
        nlp_data = self.nlp.get_data()

        if cv_data == '':
            cv_data = f'{self.__timer()} \n FaceNotFound'
        else:
            cv_data = f'{self.__timer()} \n {cv_data}'

        if nlp_data == '':
            nlp_data = f'{self.__timer()} \n AudioNotFound'
        else:
            nlp_data = f'{self.__timer()} \n {nlp_data}'

        upload = requests.patch(url=f'{setting.url}analyz/?token=Ymka',
                                json={'id': self.id, 'lid': self.lid, "audio": nlp_data, "video": cv_data})

        mark = requests.get(url=f'{setting.url}analyz/mark?id={str(self.id)}&token=Ymka')
        mark = eval(mark.text)
        mark = mark['result']
        if mark != "No":
            self.mark = mark
        # self.mark = randint(50, 100)
        mark = requests.get(url=f'{setting.url}analyz/statistic?id={str(self.id)}&token=Ymka')
        mark = mark.text
        # self.statistic = mark

    def open_secondary_window(self, event):
        if not self.secondary_window:
            # Получение размеров и позиции основного окна
            main_x = self.winfo_x()
            main_y = self.winfo_y()
            main_width = self.winfo_width()
            main_height = self.winfo_height()

            # Получение размеров экрана
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()

            # Размеры второго окна
            secondary_width = 50
            secondary_height = 50

            # Рассчитываем позицию второго окна
            if main_x + main_width + secondary_width <= screen_width:
                # Второе окно справа от основного окна
                secondary_x = main_x + main_width
                secondary_y = main_y
            else:
                # Второе окно слева от основного окна
                secondary_x = main_x - secondary_width
                secondary_y = main_y

            # Создание второго окна
            self.secondary_window = tk.Toplevel(self.master)
            self.secondary_window.geometry(f"{secondary_width}x{secondary_height}+{secondary_x}+{secondary_y+60}")
            self.secondary_window.overrideredirect(True)
            # Добавление виджетов во второе окно
            label = tk.Label(self.secondary_window, text=self.mark, font=("Arial", 16))
            label.pack(fill=tk.BOTH, expand=True)

    def close_secondary_window(self, event):
        if self.secondary_window:
            self.secondary_window.destroy()
            self.secondary_window = None

    def open_long_window(self, event):
        if not self.secondar_window:
            # Получение размеров и позиции основного окна
            main_x = self.winfo_x()
            main_y = self.winfo_y()
            main_width = self.winfo_width()
            main_height = self.winfo_height()

            # Получение размеров экрана
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()

            # Размеры второго окна
            secondary_width = 750
            secondary_height = 120

            # Рассчитываем позицию второго окна
            if main_x + main_width + secondary_width <= screen_width:
                # Второе окно справа от основного окна
                secondary_x = main_x + main_width
                secondary_y = main_y
            else:
                # Второе окно слева от основного окна
                secondary_x = main_x - secondary_width
                secondary_y = main_y

            # Создание второго окна
            self.secondar_window = tk.Toplevel(self.master)
            self.secondar_window.geometry(f"{secondary_width}x{secondary_height}+{secondary_x}+{secondary_y+95}")
            self.secondar_window.overrideredirect(True)
            y = 0
            # Добавление виджетов во второе окно
            for i in self.statistic.split("\n"):
                if self.statistic.split("\n").index(i) % 2 == 0:
                    tk.Label(self.secondar_window, text=i, font=("Arial", 16, 'bold')).place(x=0, y=y)
                else:
                    tk.Label(self.secondar_window, text=i, font=("Arial", 10)).place(x=0, y=y)
                y += 30

    def close_long_window(self, event):
        if self.secondar_window:
            self.secondar_window.destroy()
            self.secondar_window = None

    def update_secondary_window_position(self, event):
        if self.secondary_window:
            # Получение размеров и позиции основного окна
            main_x = self.winfo_x()
            main_y = self.winfo_y()
            main_width = self.winfo_width()
            main_height = self.winfo_height()

            # Получение размеров экрана
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()

            # Размеры второго окна
            secondary_width = self.secondary_window.winfo_width()
            secondary_height = self.secondary_window.winfo_height()

            # Рассчитываем позицию второго окна
            if main_x + main_width + secondary_width <= screen_width:
                # Второе окно справа от основного окна
                secondary_x = main_x + main_width
                secondary_y = main_y
            else:
                # Второе окно слева от основного окна
                secondary_x = main_x - secondary_width
                secondary_y = main_y

            # Обновляем позицию второго окна
            self.secondary_window.geometry(f"+{secondary_x}+{secondary_y}")

    def set_appwindow(self):
        hwnd = windll.user32.GetParent(self.winfo_id())
        style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        style = style & ~WS_EX_TOOLWINDOW
        style = style | WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        # re-assert the new window style
        self.wm_withdraw()
        self.after(10, lambda: self.wm_deiconify())

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def on_motion(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")


def load(stop):
    loads = Load()

    def check():
        if stop.is_set():
            loads.destroy()
        else:
            loads.after(100, check)

    check()
    loads.mainloop()


if __name__ == "__main__":
    stop_event = Event()
    gui = Thread(target=load, args=(stop_event,))
    gui.start()

    from CV.main import CV
    from NLP.main import NLP
    stop_event.set()
    gui.join()

    app = CustomWindow(cv=CV(), nlp=NLP(state=True))
    app.mainloop()
