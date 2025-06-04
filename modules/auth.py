from tkinter import ttk, Tk, StringVar

from customtkinter import (CTkFrame, CTkButton, CTkLabel,
                           CTkFont, CTkImage, CTkCanvas)

import sys, os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from setting import setting
import configparser
from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkFont, CTkImage, CTkTabview, CTkEntry
from dotmap import DotMap
import requests
from PIL import Image


class Auth(Tk):
    def __init__(self, is_internet=True, screenName=None, baseName=None, className="Tk", useTk=True, sync=False, use=None):
        super().__init__(screenName, baseName, className, useTk, sync, use)

        self.title("Авторизация")
        self.iconbitmap(default="img\\icon.ico")
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.geometry("289x228")
        self.resizable(False, False)
        self.rowconfigure(index=0, weight=1)
        self.columnconfigure(index=0, weight=1)
        self.configure(bg="white")

        self.login = StringVar(value=None)
        self.password = StringVar(value=None)

        # Авторизация
        self.frame = CTkFrame(self, width=260, height=180,
                              bg_color='white', fg_color='white')
        # self.title_ = CTkLabel(self.frame, text='Авторизация', font=CTkFont("Open Sans", 30), fg_color='white').pack()

        # Работа с логином
        self.login_frame = CTkFrame(self.frame, width=260, height=60,
                                    bg_color='white', fg_color='white')
        self.login_input = CTkEntry(self.login_frame, textvariable=self.login,
                                    corner_radius=10, border_width=1,
                                    border_color='black', fg_color='white',
                                    bg_color='white',
                                    width=260, height=35,
                                    placeholder_text='Введите email',
                                    placeholder_text_color='black').place(x=0,
                                                                          y=10)
        self.login_lable = CTkLabel(self.login_frame, text="Email",
                                    bg_color='white', fg_color='white',
                                    width=60, height=10,
                                    font=CTkFont('Open Sans', 13)).place(x=10,
                                                                         y=3)
        self.login_frame.place(x=0, y=10)

        # Работа с паролем
        self.password_frame = CTkFrame(self.frame, width=260, height=90,
                                       bg_color='white', fg_color='white')
        self.password_input = CTkEntry(self.password_frame,
                                       textvariable=self.password,
                                       corner_radius=10, border_width=1,
                                       border_color='black', fg_color='white',
                                       bg_color='white',
                                       width=260, height=35).place(x=0, y=10)
        self.password_lable = CTkLabel(self.password_frame, text="Пароль",
                                       bg_color='white', fg_color='white',
                                       width=60, height=10,
                                       font=CTkFont('Open Sans', 13)
                                       ).place(x=10, y=3)
        self.password_frame.place(x=0, y=70)

        # Работа с ошибкой пароля
        self.uninvalid_frame = CTkFrame(self.frame,
                                        bg_color='white', fg_color='white',
                                        width=260, height=20)
        if is_internet:
            text = "* Не верно введен логин или пароль"
            self.uninvalid_lable = CTkLabel(self.uninvalid_frame,
                                            text=text,
                                            font=CTkFont('Open Sans', 13),
                                            fg_color='white',
                                            bg_color='white')
        else:
            text = "* Нет интернета!"
            self.uninvalid_lable = CTkLabel(self.uninvalid_frame,
                                            text=text,
                                            font=CTkFont('Open Sans', 13),
                                            fg_color='white',
                                            bg_color='white').place(x=0, y=0)
        self.uninvalid_frame.place(x=0, y=120)

        image = Image.open(fp="img/verification.png")
        ctk_image = CTkImage(light_image=image,
                             dark_image=image,
                             size=(260, 40))

        # Запрос на авторизацию
        if is_internet:
            CTkButton(self, image=ctk_image, width=260, height=40, text="",
                      bg_color="transparent", fg_color="transparent",
                      hover_color="white", cursor="hand2",
                      command=self.auth).place(x=0, y=160)
        else:
            CTkButton(self, image=ctk_image, width=260, height=40, text="",
                      bg_color="transparent", fg_color="transparent",
                      hover_color="white", cursor="hand2",
                      default="disabled").place(x=0, y=160)
        self.frame.place(x=10, y=10)

    def auth(self):
        data = {"login": self.login.get(), "password": self.password.get()}
        result = requests.post(url='http://127.0.0.1:8000/user/verification',
                               json=data)

        if result.status_code == 200:
            config_ = configparser.ConfigParser()
            config_['user'] = {"uid": f'{result.content.decode()}'}
            setting.update_data_config(config_)
            self.dismiss()
        else:
            self.uninvalid_lable.place(x=0, y=0)

    def center_window(self):
        width = 260
        height = 282
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{260}x{282}+{x}+{y}")

    def dismiss(self):
        self.grab_release() 
        self.destroy()



if __name__ == "__main__":
    main = Auth()
    main.mainloop()