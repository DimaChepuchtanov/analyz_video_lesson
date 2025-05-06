import os


# Проверка наличия необходимых папок
def dir_os():
    """Проверка наличия папки

    ::ВЫХОДНЫЕ ДАННЫЕ
        * bool -> Будевые значения наличия необходимых папок \ файлов
    """
    has_dir = os.path.isdir('C:\\vision')
    if has_dir:
        has_setting = os.path.isfile('C:\\vision\\setting.ini')
        has_user = os.path.isfile('C:\\vision\\user.txt')
        if has_setting and has_user:
            return True
        else:
            return False
    else:
        return False


def create_dir():
    """Создание необходимых папок"""

    try:
        os.makedirs("C:\\vision")

        # Создание конфига
        config_file = open("C:\\vision\\setting.ini", "w")
        config_file.write("[general]\n")
        config_file.write("log_level = info\n")
        config_file.close()

        # Создание логирования
        logger_file = open("C:\\vision\\user.txt", "w")
        logger_file.close()
    except Exception as e:
        print("Ошибка", e)
        return False
    else:
        return True


def main():
    if dir_os():
        return True
    else:
        if create_dir():
            return True
        else:
            return False
    
