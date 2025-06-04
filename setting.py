import configparser
from password_generator import PasswordGenerator
from modules import request, directory


class Setting():
    def __init__(self, url: str | None = "http://127.0.0.1:8000/"):
        self.url = url
        self.pwo = PasswordGenerator()
        self.is_internet = request.check_internet()
        self.is_dir = directory.main()
        self.browser_path = r'C:\Users\79826\AppData\Local\Yandex\YandexBrowser\Application\browser.exe'
        self.link_meet = 'https://telemost.yandex.ru/j/30527821286466'

        if self.is_dir:
            self.config_data = self.read_data_config()

        self.loggin_lvl = self.config_data.get('general', 'log_level')

        try:
            self.user_id = self.config_data.getint("user", "uid")
        except configparser.NoSectionError:
            self.user_id = None

    def rewrite_data_config(self, new_data) -> bool:
        """Функция перезаписи данных файла config
        """

        # Write the configuration to a file
        with open('C:\\vision\\setting.ini', 'w') as configfile:
            new_data.write(configfile)

        return True

    def update_data_config(self, new_data) -> bool:
        """Функция обновления данных файла config
        """

        # Write the configuration to a file
        with open('C:\\vision\\setting.ini', 'a') as configfile:
            new_data.write(configfile)

        return True

    def read_data_config(self) -> configparser.ConfigParser:
        """Функция чтения данных из файла .config"""

        config = configparser.ConfigParser()
        try:
            config.read("C:\\vision\\setting.ini")
        except Exception:
            return {}
        else:
            return config

    def reload_user(self):
        config_data = self.read_data_config()
        try:
            user_id = config_data.getint("user", "uid")
        except Exception:
            user_id = None
        return int(user_id)


setting = Setting()
