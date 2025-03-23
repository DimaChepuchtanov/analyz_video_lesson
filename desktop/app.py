from tkinter import *
from tkinter import ttk, messagebox, PhotoImage
from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkFont, CTkImage, CTkTabview, CTkEntry
from CTkTable import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk 
from random import randint
from typing import Optional
import configparser
import os
import datetime
import threading
import sys
from PIL import Image, ImageDraw, ImageTk
import subprocess

# Подключение самописных модулей
from modules import *
from setting import *



class Main(Tk):
    def __init__(self, is_internet = False, screenName = None, baseName = None, className = "Tk", useTk = True, sync = False, use = None, uid = 0):
        super().__init__(screenName, baseName, className, useTk, sync, use)

        self.has_internet = is_internet

        # Дефолт настройки переменных
        self.list_poz = 2
        self.list_recog = []
        self.state = False

        # Настройки при отсутсвтии интернета
        if is_internet:
            self.uid = uid
        else:
            self.is_internet_thread = threading.Thread(target=schedule_internet, name="IS_INTERNET")
            self.is_internet_thread.start()
            threading.Thread(target=self.check_theard, kwargs={"id": self.is_internet_thread}).start()
            self.uid = uid

        # Задаем основные параметры окна
        self.title("Главная")
        self.iconbitmap(default="img\icon.ico")
        self.protocol("WM_DELETE_WINDOW", self.finish)
        self.geometry(f"800x620")
        self.resizable(False, False)
        self.rowconfigure(index=0, weight=1)
        self.columnconfigure(index=0, weight=1)

        # Меню
        main_menu = Menu()
        reference = Menu()
        reference.add_command(label="Справка")
        main_menu.add_cascade(label="Справка", menu=reference)

        # Задаем стили
        self.style = ttk.Style()
        self.style.configure("Main_line.TFrame", background="Black")
        self.style.configure("add_list.TFrame", background="Blue")
        self.style.configure("add_list_2.TFrame", background="Dark green")
        self.style.configure("add_list_2.TFrame", background="Dark green")

        # Фрейм записей
        self.recog_list = CTkFrame(self, width=450, height=250, corner_radius=10, fg_color="white")

        CTkLabel(self.recog_list, text=f"Записи от ", font=CTkFont("Open Sans", 16)).place(x=15, y=8)

        self.date = CTkLabel(self.recog_list, text=datetime.datetime.strftime(datetime.datetime.now(), "%d/%m/%Y"), font=CTkFont("Open Sans", 16))
        self.date.place(x=90, y=8)

        image = Image.open(fp="img\icon_data.png")
        ctk_image = CTkImage(
                            light_image=image,
                            dark_image=image,
                            size=(21, 21)
                            )
        CTkButton(self.recog_list, image=ctk_image, width=10, height=10, text="", bg_color="transparent", fg_color="transparent", hover_color="white", cursor="hand2", command=self.select_date).place(x=180, y=6)

        self.date_select = CTkFrame(self.recog_list, width=80, height=20)
        self.get_date = CTkEntry(self.date_select, width=80, height=20, placeholder_text="01/01/2025")
        self.get_date.place(x=0, y=0)

        s = CTkFrame(self.recog_list, width=420, height=100, fg_color="white")
        s.place(x=10, y=50)
        tree = CTkTable(master=s, row=6, height=30, header_color="#ebe6f7", corner_radius=9)
        tree.pack(fill=BOTH)

        tree.add_column(index=0, values=["Имя"])
        tree.add_column(index=1, values=["Оценка"])
        tree.add_column(index=2, values=["Действие"])
        tree.delete_column(3)
        tree.delete_column(3)
        self.recog_list.place(x=10, y=10)


        # Кнопка добавления записей
        self.add_subject = CTkButton(self, width=450, height=40, text="Добавить тему", fg_color="#ededed", border_width=2, corner_radius=10, font=("Arial", 16), cursor="hand2", hover_color="#3a3a3a")
        self.add_subject.place(x=10, y=270)

        #  * Список тем
        self.sub_list = CTkFrame(self, width=450, height=290, corner_radius=10, fg_color="white")

        # Настройка левой кнопки
        image = Image.open(fp="img\strelka_left.png")
        left_button = CTkImage(light_image=image, dark_image=image, size=(21, 21))
        CTkButton(self.sub_list, image=left_button, width=10, height=10, text="", bg_color="transparent", fg_color="transparent", hover_color="white", cursor="hand2", command=self.pagination_left).place(x=2, y=130)

        # Настройка правой кнопки
        image = Image.open(fp="img\strelka_right.png")
        right_button = CTkImage(light_image=image, dark_image=image, size=(21, 21))
        CTkButton(self.sub_list, image=right_button, width=10, height=10, text="", bg_color="transparent", fg_color="transparent", hover_color="white", cursor="hand2", border_spacing=4, command=self.pagination_right).place(x=413, y=130)

        # Настройка рабочего поля
        self.list_sub = CTkFrame(self.sub_list, width=390, height=240, fg_color="white")
        self.add_sub()
        self.list_sub.place(x=30, y=25)
        self.sub_list.place(x=10, y=320)

        # Оценка
        self.mark_frame = CTkFrame(self, width=120, height=120, corner_radius=10, fg_color="white")
        CTkLabel(self.mark_frame, width=114, height=20, text='Средняя оценка', font=CTkFont("Open Sans", 14)).place(x=3, y=90)

        image = Image.open(fp="img\settin.png")
        ctk_image = CTkImage(
            light_image=image,
            dark_image=image,
            size=(21, 21)  # Исходный размер изображения
        )
        CTkButton(self.mark_frame, image=ctk_image, width=10, height=10, text="", bg_color="transparent", fg_color="transparent", hover_color="white", cursor="hand2").place(x=80, y=6)
        self.mark_frame.place(x=470, y=10)

        # Пользователь
        self.user_profile = CTkFrame(self, width=190, height=120, corner_radius=10, fg_color="white")
        CTkFrame(self.user_profile, width=35, height=35, corner_radius=30, bg_color="white", border_color="gray", fg_color="white", border_width=2).place(x=80, y=5)
        CTkLabel(self.user_profile, text="Uid:0000000", font=CTkFont("Open Sans", 14), height=18).place(x=55, y=40)
        CTkLabel(self.user_profile, text="Сеть: Подключено", font=CTkFont("Open Sans", 14), height=18).place(x=35, y=60)
        CTkButton(self.user_profile, width=157, height=25, text="Выйти", fg_color="white", border_width=2, corner_radius=10, font=CTkFont("Open Sans", 14), hover_color="white", text_color="black", border_color="#3500AF", cursor="hand2", command=self.exit_auth).place(x=15, y=85)
        self.user_profile.place(x=600, y=10)

        # Недельный график
        self.week_graph = CTkFrame(self, width=320, height=200, corner_radius=10, fg_color="white")
        self.week_graph.place(x=470, y=140)

        # круговой график
        self.pie_graph = CTkFrame(self, width=320, height=200, corner_radius=10, fg_color="white")
        self.pie_graph.place(x=470, y=350)

        # Кнопка записи
        image = Image.open(fp="img\start_recog.png")
        ctk_image = CTkImage(
            light_image=image,
            dark_image=image,
            size=(320, 48)  # Исходный размер изображения
        )
        CTkButton(self, image=ctk_image, width=320, height=48, text="", bg_color="transparent", fg_color="transparent", hover_color="#ededed", cursor="hand2", command=self.start_recog).place(x=462, y=560)

    def exit_auth(self):
        """Выход из учетной записи"""
        config_ = configparser.ConfigParser()
        config_['general'] = {"log_level": "info"}
        remove_data_config(config_)
        self.destroy()

    def select_date(self):

        if self.state:
            print(self.get_date.get())
            self.date.configure(text=self.get_date.get())
            self.date_select.place_forget()
            self.get_date.delete(0, END)
            self.state = False
        else:
            try:
                self.date_select.place(x=230, y=6)
            except:
                self.date_select.configure(state='enable')
            finally:
                self.state = True

    def add_sub(self):
        """Получение данных записей из файла или базы данных"""


        if self.has_internet is not True:
            pass
        else:
        # Сценарий для чтения из файла
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
            s = CTkFrame(self.list_sub, width=190, height=240, border_width=1, border_color='black', corner_radius=15, fg_color="white")

            CTkFrame(s, width=160, height=70, border_width=1, border_color='black', fg_color="white", corner_radius=10).place(x=15, y=10)
            CTkLabel(s, width=100, text=f"Тема: {self.list_recog[i][3]}", font=("Open Sans", 18)).place(x=20, y=80)
            CTkLabel(s, width=100, text="Длительность:", font=("Open Sans", 20, "bold")).place(x=20, y=128)
            CTkLabel(s, width=100, text=f"{self.list_recog[i][2]}", font=CTkFont("Open Sans", 14)).place(x=47, y=153)

            image = Image.open(fp="img\\more_info.png")
            CTkButton(s,
                      image=CTkImage(light_image=image, dark_image=image, size=(95, 30)),
                      width=95, height=30, text="", bg_color="transparent", fg_color="transparent", hover_color="white", cursor="hand2", border_spacing=4).place(x=10, y=185)

            image = Image.open(fp="img\\del.png")
            CTkButton(s,
                      image=CTkImage(light_image=image, dark_image=image, size=(30, 30)),
                      width=30, height=30, text="", bg_color="transparent", fg_color="transparent", hover_color="white", cursor="hand2", border_spacing=4).place(x=120, y=182)
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
            s = CTkFrame(self.list_sub, width=190, height=240, border_width=1, border_color='black', corner_radius=15, fg_color="white")

            CTkFrame(s, width=160, height=70, border_width=1, border_color='black', fg_color="white", corner_radius=10).place(x=15, y=10)
            CTkLabel(s, width=100, text=f"Тема: {self.list_recog[i][3]}", font=("Open Sans", 18)).place(x=20, y=80)
            CTkLabel(s, width=100, text="Длительность:", font=("Open Sans", 20, "bold")).place(x=20, y=128)
            CTkLabel(s, width=100, text=f"{self.list_recog[i][2]}", font=CTkFont("Open Sans", 14)).place(x=47, y=153)

            image = Image.open(fp="img\\more_info.png")
            CTkButton(s,
                      image=CTkImage(light_image=image, dark_image=image, size=(95, 30)),
                      width=95, height=30, text="", bg_color="transparent", fg_color="transparent", hover_color="white", cursor="hand2", border_spacing=4).place(x=10, y=185)

            image = Image.open(fp="img\\del.png")
            CTkButton(s,
                      image=CTkImage(light_image=image, dark_image=image, size=(30, 30)),
                      width=30, height=30, text="", bg_color="transparent", fg_color="transparent", hover_color="white", cursor="hand2", border_spacing=4).place(x=120, y=182)
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
            s = CTkFrame(self.list_sub, width=190, height=240, border_width=1, border_color='black', corner_radius=15, fg_color="white")

            CTkFrame(s, width=160, height=70, border_width=1, border_color='black', fg_color="white", corner_radius=10).place(x=15, y=10)
            CTkLabel(s, width=100, text=f"Тема: {self.list_recog[i][3]}", font=("Open Sans", 18)).place(x=20, y=80)
            CTkLabel(s, width=100, text="Длительность:", font=("Open Sans", 20, "bold")).place(x=20, y=128)
            CTkLabel(s, width=100, text=f"{self.list_recog[i][2]}", font=CTkFont("Open Sans", 14)).place(x=47, y=153)

            image = Image.open(fp="img\\more_info.png")
            CTkButton(s,
                      image=CTkImage(light_image=image, dark_image=image, size=(95, 30)),
                      width=95, height=30, text="", bg_color="transparent", fg_color="transparent", hover_color="white", cursor="hand2", border_spacing=4).place(x=10, y=185)

            image = Image.open(fp="img\\del.png")
            CTkButton(s,
                      image=CTkImage(light_image=image, dark_image=image, size=(30, 30)),
                      width=30, height=30, text="", bg_color="transparent", fg_color="transparent", hover_color="white", cursor="hand2", border_spacing=4).place(x=120, y=182)
            s.place(x=pos_x, y=pos_y)
            pos_x += 200
        return True

    def create_gradient_image(self, width, height, start_color, end_color, radius):
        gradient = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(gradient)

        for y in range(height):
            r = int(start_color[0] + (end_color[0] - start_color[0]) * y / height)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * y / height)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * y / height)
            draw.line([(0, y), (width, y)], fill=(r, g, b, 1))

         # Создаем маску для закругленных углов
        mask = Image.new('L', (width, height), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.rounded_rectangle([0, 0, width, height], radius=radius, fill=255)

        # Применяем маску к изображению
        gradient.putalpha(mask)
        return gradient

    # Заполнение данных раздела "Графики"
    def show_info_graph(self):
        data = []
        if self.has_internet:
            pass
            mark = 0
        else:
            data = ""
            try:
                with open("C:\\vision\\rec.txt", 'r', encoding='utf-8') as f:
                    data = f.readlines()
            except FileNotFoundError:
                self.mark.itemconfig(self.text_mark_edit, text="0")
                return

        if len(data) == 0:
            labels = []
            sizes = []
            colors = []
            explode = ()  # "выпуклость" первого сектора (яблоки)
            return

        # Создание круговой диаграммы
        mark = [int(x.removesuffix("\n").split("; ")[1].removesuffix(";")) for x in data]
        labels = list(str(x) for x in set(mark))
        sizes = [mark.count(int(x)) for x in labels]
        colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue'][:len(labels)]
        figure = Figure(figsize=(1.5, 1.5))
        ax = figure.add_subplot(111)

        ax.pie(sizes, labels=labels, colors=colors, shadow=True)
        figure.set_facecolor('#f0f0f0')
        ax.axis('equal')
        canvas = FigureCanvasTkAgg(figure, master=self.diagramm)
        canvas.draw()
        canvas.get_tk_widget().place(x=5+161+12+5, y=6)
        ttk.Label(self.diagramm, text="Оценки").place(x=234, y=155)

        # Создание линейного графика
        # day_week = ['Понедельник', "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

        # dict_value = {}
        # mark = [[int(x.removesuffix("\n").split("; ")[1].removesuffix(";")), x.removesuffix("\n").split("; ")[2].removesuffix(";")] for x in data]
        # for i in mark:
        #     if i[1] not in dict_value:
        #         dict_value[i[1]] = 1
        #     else:
        #         dict_value[i[1]] = dict_value[i[1]] + 1

        # labels = [datetime.datetime.strptime(x, "%d-%m-%Y").weekday() for x in dict_value.keys()]
        # sizes = list(dict_value.values())
        # colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue'][:len(labels)]
        # figure = Figure(figsize=(4, 2), dpi=75)
        # ax = figure.add_subplot(111)

        # ax.plot(labels, sizes, c='r')
        # figure.set_facecolor('#f0f0f0')
        # canvas = FigureCanvasTkAgg(figure, master=self.diagramm)
        # canvas.draw()
        # canvas.get_tk_widget().place(x=340, y=6)
        # ttk.Label(self.diagramm, text="Кол-во записей на неделе").place(x=425, y=155)

        # Создание столбчатого
        labels = ['Online', "Offline"]
        sizes = [50, 20]
        figure = Figure(figsize=(2, 2), dpi=74)
        ax = figure.add_subplot(111)

        ax.bar(labels, sizes)
        figure.set_facecolor('#f0f0f0')
        canvas = FigureCanvasTkAgg(figure, master=self.diagramm)
        canvas.draw()
        canvas.get_tk_widget().place(x=650, y=6)
        ttk.Label(self.diagramm, text="Кол-во записей").place(x=680, y=155)

    # Заполнение данных раздела "Оценка"
    def show_info_mark(self):

        if self.has_internet:
            pass
            mark = 0
        else:
            data = ""
            try:
                with open("C:\\Program Files\\vision\\rec.txt", 'r', encoding='utf-8') as f:
                    data = f.readlines()
            except FileNotFoundError:
                self.mark.itemconfig(self.text_mark_edit, text="NaN")
                return

            if len(data) == 0:
                self.mark.itemconfig(self.text_mark_edit, text="0")
                return

            mark = [int(x.removesuffix("\n").split("; ")[1].removesuffix(";")) for x in data]
            mark = int(sum(mark)/len(mark))

        self.mark.itemconfig(self.text_mark_edit, text=mark)
        return

    # Заполнение данных раздела "Записи"
    def show_info_recognize(self):

        if self.has_internet:
            pass
        else:
            data = ""
            try:
                with open("C:\\Program Files\\vision\\rec.txt", 'r', encoding='utf-8') as f:
                    data = f.readlines()
            except FileNotFoundError:
                return

            if len(data) == 0:
                return

            count = 8 if len(data) > 8 else len(data)
            for i in range(0,count):
                information = data[i].removesuffix("\n").split("; ")
                information[1] = information[1].removesuffix(";")
                self.tree.insert("", END, values=(information[0], information[1], "Действие"))
        return

    def check_theard(self, id: threading.Thread):
        while id.is_alive():
            pass

        # Тут нужно сделать запуск скрипта вывода данных в базу по обнаружению интернета
        self.profile.itemconfig(self.status_user, text="active", fill="#03FF31")


    def start_recog(self):
        self.destroy()
        subprocess.Popen(["python", "modules/noname.py"])


    def finish(self):
        self.destroy()  # ручное закрытие окна и всего приложения
        print("Закрытие приложения")

    def dismiss(self):
        self.grab_release() 
        self.destroy()
        sys.exit()




if __name__ == "__main__":
    # Проверка на авторизацию пользователя
    if user_id is None:
        auth_ = Auth(is_internet=is_internet)
        auth_.mainloop()
        user_id = reload_user()

    # Повторная провека
    if user_id is None:
        exit()

    # Запуск главного окна

    main = Main(is_internet=is_internet, uid=user_id)
    main.mainloop()