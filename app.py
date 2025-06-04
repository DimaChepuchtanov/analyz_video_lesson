from tkinter import (ttk, Toplevel,
                     Tk as Tkinter,
                     BOTH as BOTH_)

from customtkinter import (CTkFrame, CTkButton, CTkLabel,
                           CTkFont, CTkImage, CTkCanvas)


import CTkTable as CTable
from tkcalendar import Calendar
import configparser
import os
import datetime
import threading
import sys
from PIL import Image
from random import randint
import subprocess
import numpy as np
from requests import get
from statistics import mean


# Подключение самописных модулей
from modules import (auth as auth_module,
                     request)
from setting import (setting)


class Main(Tkinter):
    def __init__(self, is_internet=False, screenName=None, baseName=None,
                 className="Tk", useTk=True, sync=False, use=None, uid=0):
        super().__init__(screenName, baseName, className, useTk, sync, use)

        self.has_internet = is_internet
        self.config_ = configparser.ConfigParser()
        # Дефолт настройки переменных
        self.list_poz = 2
        self.list_recog = []
        self.state = False

        h, k = 37.5, 37
        r = 32.5
        theta = np.linspace(0, 2*np.pi, 100)
        self.x = h + r * np.cos(theta)
        self.y = k + r * np.sin(theta)
        d = [[xz, yz] for xz, yz in zip(self.x, self.y)]
        self.cood = [x for x in d[25:]] + [x for x in d[:25]]

        #  Настройки при отсутсвтии интернета
        if is_internet:
            self.uid = uid
        else:
            self.is_internet_thread = threading.Thread(target=request.check_internet,
                                                       name="IS_INTERNET")
            self.is_internet_thread.start()
            threading.Thread(target=self.check_theard,
                             kwargs={"id": self.is_internet_thread}).start()
            self.uid = uid

        # Задаем основные параметры окна
        self.title("Главная")
        self.iconbitmap(default="img\\icon.ico")
        self.protocol("WM_DELETE_WINDOW", self.finish)
        self.geometry("800x620")
        self.resizable(False, False)
        self.rowconfigure(index=0, weight=1)
        self.columnconfigure(index=0, weight=1)
        self.configure(bg="#ECECEC")

        # Задаем стили
        self.style = ttk.Style()
        self.style.configure("Main_line.TFrame", background="Black")
        self.style.configure("add_list.TFrame", background="Blue")
        self.style.configure("add_list_2.TFrame", background="Dark green")
        self.style.configure("add_list_2.TFrame", background="Dark green")

        # Фрейм записей
        self.recog_list = CTkFrame(self, width=450, height=250,
                                   corner_radius=10, fg_color="#F6F6F6")

        CTkLabel(self.recog_list, text="Записи от ",
                 font=CTkFont("Open Sans", 16)).place(x=15, y=8)

        self.date = CTkLabel(self.recog_list,
                             text=datetime.datetime.strftime(datetime.datetime.now(), "%d/%m/%Y"),
                             font=CTkFont("Open Sans", 16))
        self.date.place(x=90, y=8)

        image = Image.open(fp="img\\icon_data.png")
        ctk_image = CTkImage(light_image=image,
                             dark_image=image,
                             size=(21, 21))

        CTkButton(self.recog_list, image=ctk_image, width=10, height=10,
                  text="", bg_color="transparent", fg_color="transparent",
                  hover_color="white", cursor="hand2",
                  command=self.open_calendar).place(x=180, y=6)

        s = CTkFrame(self.recog_list, width=420, height=100,
                     fg_color="#F6F6F6", bg_color='#F6F6F6',
                     corner_radius=60)
        s.place(x=10, y=50)

        value = []
        marke = 0
        table_lessons = get('http://127.0.0.1:8000/lesson/?token=Ymka&filter=top')
        if table_lessons.status_code == 200:
            value = eval(table_lessons.content)
            marke = mean([x[1] for x in value])
        self.tree = CTable.CTkTable(master=s, row=6, height=30,
                                    pady=1, column=3,
                                    header_color="#ebe6f7",
                                    colors=['white', 'white'],
                                    corner_radius=10,
                                    bg_color='#F6F6F6',
                                    fg_color='#F6F6F6')
        self.tree.pack(fill=BOTH_)
        self.tree.add_column(index=0, values=["Имя"])
        self.tree.add_column(index=1, values=["Оценка"])
        self.tree.add_column(index=2, values=["Действие"])
        for i in range(len(value)):
            self.tree.insert(i+1, 0, value[i][0])
            self.tree.insert(i+1, 1, value[i][1])
            self.tree.insert(i+1, 2, value[i][2])

        self.tree.delete_column(3)
        self.tree.delete_column(3)
        self.tree.delete_column(3)

        self.recog_list.place(x=10, y=10)

        #  Кнопка добавления записей
        self.add_subject = CTkButton(self, width=450, height=40,
                                     text="", fg_color="#F6F6F6",
                                     border_width=2, corner_radius=10,
                                     font=("Arial", 16),
                                     hover_color="white")
        self.add_subject.place(x=10, y=270)

        #  * Список тем
        self.sub_list = CTkFrame(self, width=450, height=290,
                                 corner_radius=10, fg_color="#F6F6F6")

        # Настройка левой кнопки
        image = Image.open(fp="img\\strelka_left.png")
        left_button = CTkImage(light_image=image,
                               dark_image=image,
                               size=(21, 21))
        CTkButton(self.sub_list, image=left_button, width=10, height=10,
                  text="", bg_color="transparent", fg_color="transparent",
                  hover_color="#F6F6F6", cursor="hand2",
                  command=self.pagination_left).place(x=2, y=130)

        # Настройка правой кнопки
        image = Image.open(fp="img\\strelka_right.png")
        right_button = CTkImage(light_image=image,
                                dark_image=image,
                                size=(21, 21))
        CTkButton(self.sub_list, image=right_button, width=10, height=10,
                  text="", bg_color="transparent", fg_color="transparent",
                  hover_color="#F6F6F6", cursor="hand2", border_spacing=4,
                  command=self.pagination_right).place(x=413, y=130)

        # Настройка рабочего поля
        self.list_sub = CTkFrame(self.sub_list, width=390,
                                 height=240, fg_color="#F6F6F6")
        self.add_sub()
        self.list_sub.place(x=30, y=25)
        self.sub_list.place(x=10, y=320)

        # Оценка
        self.mark_frame = CTkFrame(self, width=120, height=120,
                                   corner_radius=10, fg_color="#F6F6F6")

        CTkLabel(self.mark_frame, width=114, height=20, text='Средняя оценка',
                 font=CTkFont("Open Sans", 14)).place(x=3, y=90)

        image = Image.open(fp="img\\settin.png")
        ctk_image = CTkImage(light_image=image,
                             dark_image=image,
                             size=(17, 17))

        CTkButton(self.mark_frame, image=ctk_image, width=10, height=10,
                  text="", bg_color="transparent", fg_color="transparent",
                  hover_color="#F6F6F6", cursor="hand2",
                  command=self.open_range_picker).place(x=86, y=6)

        self.mark_frame.place(x=470, y=10)

        self.mark = CTkCanvas(self.mark_frame, width=73, height=75,
                              background='#F6F6F6', bg='#F6F6F6',
                              borderwidth=0,
                              insertborderwidth=0, selectborderwidth=0,
                              bd=0, highlightthickness=0, relief='ridge')
        self.mark.place(x=15, y=10)

        self.update_label_mark(marke)

        # Пользователь
        self.user_profile = CTkFrame(self, width=190, height=120,
                                     corner_radius=10, fg_color="#F6F6F6")

        CTkFrame(self.user_profile, width=35, height=35, corner_radius=30,
                 bg_color="#F6F6F6", border_color="gray", fg_color="#F6F6F6",
                 border_width=2).place(x=80, y=5)

        CTkLabel(self.user_profile, text=f"Uid: {str(self.uid).zfill(7)}",
                 font=CTkFont("Open Sans", 14), height=18).place(x=55, y=40)

        CTkLabel(self.user_profile, text="Сеть: Подключено",
                 font=CTkFont("Open Sans", 14), height=18).place(x=35, y=60)

        CTkButton(self.user_profile, width=157, height=25, text="Выйти",
                  fg_color="#F6F6F6", border_width=2, corner_radius=10,
                  font=CTkFont("Open Sans", 14), hover_color="white",
                  text_color="black", border_color="#3500AF", cursor="hand2",
                  command=self.exit_auth).place(x=15, y=85)
        self.user_profile.place(x=600, y=10)

        # Недельный график
        self.week_graph = CTkFrame(self, width=320, height=200,
                                   corner_radius=10, fg_color="#F6F6F6")

        self.canvas = CTkCanvas(self.week_graph, bg="#F6F6F6",
                                highlightthickness=0)
        self.canvas.place(x=0, y=0)
        self.week_graph.place(x=470, y=140)
        data = self.get_lessons(tag='day')
        self.draw_chart(data)

        # bar график
        self.bar_graph = CTkFrame(self, width=320, height=200,
                                  corner_radius=10, fg_color="#F6F6F6")
        self.bar_graph.place(x=470, y=350)
        self.draw_bar([20, 40, 100])

        # Кнопка записи
        image = Image.open(fp="img\\start_recog.png")
        ctk_image = CTkImage(light_image=image,
                             dark_image=image,
                             size=(320, 48))

        CTkButton(self, image=ctk_image, width=320, height=48, text="",
                  bg_color="transparent", fg_color="transparent",
                  hover_color="#ededed", cursor="hand2",
                  command=self.start_recog).place(x=462, y=560)


    def get_lessons(self, tag: str) -> list:
        result = []
        if tag == 'day':
            day = datetime.datetime.today().weekday()
            result = [randint(0, 10) for x in range(7)]
            # for i in range(day, 7):
            #     result.append(0)

        return result

    def get_mark_with_range(self, date: dict) -> None:
        # date: start=> dd.mm.yy; end=> dd.mm.yy
        # get_ = get('http://127.0.0.1:8000/lesson/mark?start={date["start"]};
        # end={date["end"]}')
        # if get_.status_code != 200:
        #     self.update_label_mark(0)
        # else:
        #     self.update_label_mark(int(get_.text))

        self.update_label_mark(randint(0, 100))

    def update_label_mark(self, vsalue):
        self.mark.delete('all')
        self.mark.create_oval(5, 70, 70, 5, width=5, outline='#E3E3E3')
        self.mark.create_text(37.5, 36, text=f"{vsalue}",
                              font=CTkFont('Arial', 33))

        if vsalue < 50:
            self.mark.create_line(self.cood[:vsalue], smooth=True,
                                  width=5, fill='red')
            self.mark.create_rectangle(9, 55, 67, 74, fill='red',
                                       outline='#F6F6F6')
            self.mark.create_text(37, 65, text="Low",
                                  font=CTkFont('Arial', 12))
        elif vsalue < 75:
            self.mark.create_line(self.cood[:vsalue], smooth=True,
                                  width=5, fill='#FFBF7E')
            self.mark.create_rectangle(9, 55, 67, 74, fill='#FFBF7E',
                                       outline='#F6F6F6')
            self.mark.create_text(37, 65, text="Medium",
                                  font=CTkFont('Arial', 12))
        else:
            self.mark.create_line(self.cood[:vsalue],
                                  smooth=True, width=5,
                                  fill='green')
            self.mark.create_rectangle(9, 55, 67, 74, fill='green',
                                       outline='#F6F6F6')
            self.mark.create_text(37, 65, text="High",
                                  font=CTkFont('Arial', 12))

    def draw_chart(self, data):
        # Параметры области рисования
        padding = 20
        chart_width = 320 - 2*padding
        chart_height = 150 - 2*padding
        max_value = max(data) or 1
        days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]

        # Отрисовка сетки
        for i in range(0, 11, 2):
            y = padding + (chart_height * (1 - i/10))
            self.canvas.create_line(padding, y,
                                    320 - padding, y,
                                    fill="#e0e0e0",
                                    dash=(2, 2))

        # Оси координат
        self.canvas.create_line(padding, 180 - padding,
                                320 - padding, 180 - padding,
                                width=2,
                                fill="#404040")

        # Рассчет координат точек
        points = []
        for i, value in enumerate(data):
            x = padding + (chart_width * i / (len(data)-1))
            y = 180 - padding - (value/max_value * chart_height)
            points.append((x, y))

            # Подписи дней
            self.canvas.create_text(x, 180 - padding + 10,
                                    text=days[i],
                                    font=("Arial", 12),
                                    fill="#606060")

        # Линия графика
        for i in range(len(points)-1):
            self.canvas.create_line(*points[i], *points[i+1],
                                    fill="#C29FFF",
                                    width=3,
                                    smooth=True)

        # Точки данных
        for x, y in points:
            self.canvas.create_oval(x-6, y-6, x+6, y+6,
                                    fill="#5E27BC",
                                    outline="#F6F6F6",
                                    width=2)
            self.canvas.create_text(x, y-20,
                                    text=str(data[points.index((x, y))]),
                                    font=("Arial", 12, "bold"),
                                    fill="#5E27BC")

    def draw_bar(self, data=[20, 30, 50]):
        h, k = 95, 95
        r = 90
        theta = np.linspace(0, 2*np.pi, 100)
        self.x = h + r * np.cos(theta)
        self.y = k + r * np.sin(theta)
        d = [[xz, yz] for xz, yz in zip(self.x, self.y)]
        cood = [x for x in d[25:]] + [x for x in d[:25]]

        r = 60
        theta = np.linspace(0, 2*np.pi, 100)
        self.x = h + r * np.cos(theta)
        self.y = k + r * np.sin(theta)
        d = [[xz, yz] for xz, yz in zip(self.x, self.y)]
        cood2 = [x for x in d[25:]] + [x for x in d[:25]]

        r = 30
        theta = np.linspace(0, 2*np.pi, 100)
        self.x = h + r * np.cos(theta)
        self.y = k + r * np.sin(theta)
        d = [[xz, yz] for xz, yz in zip(self.x, self.y)]
        cood3 = [x for x in d[25:]] + [x for x in d[:25]]

        # Данные тем
        subjects = [
            {"name": "Математика", "color": "#FF6B6B"},
            {"name": "Русский язык", "color": "#4ECDC4"},
            {"name": "Физика", "color": "#45B7D1"}
        ]

        subject_frame = CTkFrame(self.bar_graph, fg_color="transparent",
                                 width=130, height=100)

        for idx, subject in enumerate(subjects):
            # Цветной индикатор
            CTkLabel(
                subject_frame,
                text="",
                width=20,
                height=30,
                fg_color=subject["color"],
                corner_radius=4
            ).place(x=5, y=idx*33)

            # Название темы
            CTkLabel(
                subject_frame,
                text=subject["name"],
                font=("Arial", 16),
                text_color="#2A3F5F"
            ).place(x=30, y=idx*33)
        subject_frame.place(x=0, y=10)

        line_frame = CTkCanvas(self.bar_graph, width=190, height=190,
                               bg="#F6F6F6", highlightthickness=0)
        cod = [cood, cood2, cood3]
        for idx, subject in enumerate(subjects):
            line_frame.create_line(cod[idx][:data[idx]], smooth=True,
                                   width=10, fill=subject["color"])
        line_frame.place(x=130, y=0)

    def open_calendar(self):
        # Создание модального окна
        top = Toplevel(self)
        top.title("Календарь")
        top.grab_set()  # Блокировка основного окна

        # Добавление календаря
        cal = Calendar(
            top,
            selectmode='day',
            date_pattern='dd.mm.yyyy',
            locale='ru_RU'
        )
        cal.pack(padx=10, pady=10)

        # Кнопка подтверждения выбора
        btn_ok = ttk.Button(
            top,
            text="OK",
            command=lambda: self.set_date(cal.get_date(), top)
        )
        btn_ok.pack(pady=10)

    def set_date(self, date, window):
        date = date.split('.')
        self.date.configure(text=f'{date[0]}/{date[1]}/{date[2]}')
        window.destroy()

    def open_range_picker(self):
        # Создание модального окна
        top = Toplevel(self)
        top.title("Выбор диапазона")
        top.grab_set()

        # Фрейм для календарей
        calendar_frame = ttk.Frame(top)
        calendar_frame.pack(padx=10, pady=10)

        # Календарь для начальной даты
        self.cal_start = Calendar(
            calendar_frame,
            selectmode='day',
            date_pattern='dd.mm.yyyy',
            locale='ru_RU'
        )
        self.cal_start.grid(row=0, column=0, padx=10)
        ttk.Label(calendar_frame, text="Начальная дата").grid(row=1, column=0)

        # Календарь для конечной даты
        self.cal_end = Calendar(
            calendar_frame,
            selectmode='day',
            date_pattern='dd.mm.yyyy',
            locale='ru_RU'
        )
        self.cal_end.grid(row=0, column=1, padx=10)
        ttk.Label(calendar_frame, text="Конечная дата").grid(row=1, column=1)

        # Кнопка подтверждения
        btn_confirm = ttk.Button(
            top,
            text="Подтвердить",
            command=lambda: self.set_date_range(top)
        )
        btn_confirm.pack(pady=10)

    def set_date_range(self, top):
        start = self.cal_start.get_date()
        end = self.cal_end.get_date()

        # Преобразование в объекты datetime для сравнения
        try:
            start_date = datetime.datetime.strptime(start, "%d.%m.%Y")
            end_date = datetime.datetime.strptime(end, "%d.%m.%Y")

            if start_date > end_date:
                start, end = end, start  # Меняем местами если нужно

            self.get_mark_with_range({"start": datetime.datetime.strftime(start_date, "%d.%m.%y"),
                                      "end": datetime.datetime.strftime(end_date, "%d.%m.%y")})

            top.destroy()

        except ValueError:
            top.destroy()

    def exit_auth(self):
        """Выход из учетной записи"""
        self.config_['general'] = {"log_level": "info"}
        setting.rewrite_data_config(self.config_)
        self.destroy()

    def add_sub(self):
        """Получение данных записей из файла или базы данных"""

        if self.has_internet is not True:
            pass
        else:
            try:
                with open("C:\\vision\\rec.txt", 'r', encoding='utf-8') as f:
                    temp_result = f.readlines()
            except FileNotFoundError:
                print("Ошибка чтения файла записей")
                return False
            else:
                for i in range(1, len(temp_result)):
                    temp_data = temp_result[i].strip().split(";")
                    temp_time = datetime.datetime.strptime(temp_data[2], "%H:%M")
                    hours = "час" if int(temp_time.hour) == 1 else "часа" if 2 <= int(temp_time.hour) <= 4 else "часов"
                    temp_data[2] = f"{temp_time.hour} {hours} {temp_time.minute} минут"
                    self.list_recog.append(temp_data)

        pos_x, pos_y = 0, 0
        max_len = 2 if len(self.list_recog) > 2 else len(self.list_recog)
        for i in range(0, max_len):
            s = CTkFrame(self.list_sub,
                         width=190, height=240,
                         border_width=1, border_color='black',
                         corner_radius=15, fg_color="white")

            CTkFrame(s, width=160, height=70,
                     border_width=1, border_color='black',
                     fg_color="white", corner_radius=10).place(x=15, y=10)

            CTkLabel(s, width=100,
                     text=f"Тема: {self.list_recog[i][3]}",
                     font=("Open Sans", 18)).place(x=20, y=80)

            CTkLabel(s, width=100, text="Длительность:",
                     font=("Open Sans", 20, "bold")).place(x=20, y=128)

            CTkLabel(s, width=100, text=f"{self.list_recog[i][2]}",
                     font=CTkFont("Open Sans", 14)).place(x=47, y=153)

            image = Image.open(fp="img\\more_info.png")
            CTkButton(s,
                      image=CTkImage(light_image=image,
                                     dark_image=image,
                                     size=(150, 35)),
                      width=150, height=35,
                      text="", bg_color="transparent",
                      fg_color="transparent",
                      hover_color="white",
                      cursor="hand2", border_spacing=4).place(x=5, y=185)
            s.place(x=pos_x, y=pos_y)
            pos_x += 200
        return True

    def pagination_right(self):
        """Переключение списка"""

        start_p = 0
        end_p = self.list_poz

        end_p = self.list_poz + 1 if len(self.list_recog) >= self.list_poz + 1 else self.list_poz
        start_p = end_p - 2
        self.list_poz = end_p

        pos_x, pos_y = 0, 0
        for i in range(start_p, end_p):
            s = CTkFrame(self.list_sub, width=190, height=240,
                         border_width=1, border_color='black',
                         corner_radius=15, fg_color="white")

            CTkFrame(s, width=160, height=70,
                     border_width=1, border_color='black',
                     fg_color="white", corner_radius=10).place(x=15, y=10)

            CTkLabel(s, width=100, text=f"Тема: {self.list_recog[i][3]}",
                     font=("Open Sans", 18)).place(x=20, y=80)

            CTkLabel(s, width=100, text="Длительность:",
                     font=("Open Sans", 20, "bold")).place(x=20, y=128)

            CTkLabel(s, width=100, text=f"{self.list_recog[i][2]}",
                     font=CTkFont("Open Sans", 14)).place(x=47, y=153)

            image = Image.open(fp="img\\more_info.png")
            CTkButton(s,
                      image=CTkImage(light_image=image,
                                     dark_image=image,
                                     size=(150, 35)),
                      width=150, height=35,
                      text="", bg_color="transparent",
                      fg_color="transparent",
                      hover_color="white",
                      cursor="hand2", border_spacing=4).place(x=5, y=185)

            s.place(x=pos_x, y=pos_y)
            pos_x += 200
        return True

    def pagination_left(self):

        start_p = 0
        end_p = self.list_poz

        end_p = self.list_poz - 1 if end_p - 3 >= 0 else self.list_poz
        start_p = end_p - 2
        self.list_poz = end_p

        pos_x, pos_y = 0, 0
        for i in range(start_p, end_p):
            s = CTkFrame(self.list_sub, width=190, height=240,
                         border_width=1, border_color='black',
                         corner_radius=15, fg_color="white")

            CTkFrame(s, width=160, height=70,
                     border_width=1, border_color='black',
                     fg_color="white", corner_radius=10).place(x=15, y=10)

            CTkLabel(s, width=100, text=f"Тема: {self.list_recog[i][3]}",
                     font=("Open Sans", 18)).place(x=20, y=80)

            CTkLabel(s, width=100, text="Длительность:",
                     font=("Open Sans", 20, "bold")).place(x=20, y=128)

            CTkLabel(s, width=100, text=f"{self.list_recog[i][2]}",
                     font=CTkFont("Open Sans", 14)).place(x=47, y=153)

            image = Image.open(fp="img\\more_info.png")
            CTkButton(s,
                      image=CTkImage(light_image=image,
                                     dark_image=image,
                                     size=(150, 35)),
                      width=150, height=35,
                      text="", bg_color="transparent",
                      fg_color="transparent",
                      hover_color="white",
                      cursor="hand2", border_spacing=4).place(x=5, y=185)

            s.place(x=pos_x, y=pos_y)
            pos_x += 200
        return True

    def check_theard(self, id: threading.Thread):
        while id.is_alive():
            pass

        self.profile.itemconfig(self.status_user,
                                text="active",
                                fill="#03FF31")

    def start_recog(self):
        self.destroy()
        subprocess.run(["python", f'{os.getcwd()}/modules/noname.py'])

    def finish(self):
        self.destroy()  # ручное закрытие окна и всего приложения
        print("Закрытие приложения")

    def dismiss(self):
        self.grab_release()
        self.destroy()
        sys.exit()


if __name__ == "__main__":
    # Проверка на авторизацию пользователя
    if setting.user_id is None:
        auth_ = auth_module()
        auth_.mainloop()
        setting.user_id = setting.reload_user()

    # Повторная провека
    if setting.user_id is None:
        exit()

    # Запуск главного окна
    main = Main(is_internet=setting.is_internet, uid=setting.user_id)
    main.mainloop()
