from tkinter import *
from tkinter import ttk
from .config import update_data_config
import configparser
from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkFont, CTkImage, CTkTabview, CTkEntry
from .database import get_auth
from dotmap import DotMap


class Auth(Tk):
    def __init__(self, is_internet=True, screenName = None, baseName = None, className = "Tk", useTk = True, sync = False, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)

        self.title("Авторизация")
        self.protocol("WM_DELETE_WINDOW", lambda: self.dismiss())

        self.center_window()
        self.resizable(False, False)
        self.grab_set()

        self.login = StringVar(value=None)
        self.password = StringVar(value=None)

        self.current_login = "root"
        self.current_password = "root"

        # Авторизация
        self.frame = ttk.Frame(self, borderwidth=1)
        self.title_ = CTkLabel(self.frame, text='Авторизация', font=CTkFont("Open Sans", 30)).pack()

        # Работа с логином
        self.login_frame = ttk.Frame(self.frame, style="TP.TFrame")
        self.login_lable = ttk.Label(self.login_frame, text="Логин").pack()
        self.login_input = Entry(self.login_frame, textvariable=self.login).pack()
        self.login_frame.pack()

        # Работа с паролем
        self.password_frame = ttk.Frame(self.frame, style="TP.TFrame")
        self.password_lable = ttk.Label(self.password_frame, text="Пароль").pack()
        self.password_input = ttk.Entry(self.password_frame, textvariable=self.password).pack()
        self.password_frame.pack(pady=20)

        # Работа с ошибкой пароля
        self.uninvalid_frame = ttk.Frame(self.frame, style="TP.TFrame")
        if is_internet:
            self.uninvalid_lable = ttk.Label(self.uninvalid_frame, text="* Не верно введен логин или пароль! ")
        else:
            self.uninvalid_lable = ttk.Label(self.uninvalid_frame, text="* Нет интернета! ").pack()
        self.uninvalid_frame.pack(pady=20)

        # Запрос на авторизацию
        if is_internet:
            self.btm = ttk.Button(self.frame, text="Войти", command=self.auth).pack(fill=X)
        else:
            self.btm = ttk.Button(self.frame, text="Войти", command=self.auth, default="disabled").pack(fill=X)
        self.frame.pack(expand=True)

    def auth(self):
        result = DotMap(get_auth(data={"login": self.login.get(), "password": self.password.get()}))

        if result.status_code == 200:
            config_ = configparser.ConfigParser()
            config_['user'] = {"uid": "0000001"}
            update_data_config(config_)
            self.dismiss()
        else:
            self.uninvalid_lable.pack()


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