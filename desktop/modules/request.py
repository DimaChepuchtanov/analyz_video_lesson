from urllib.request import urlopen
from urllib.error import URLError
import time
import threading


def check_internet() -> bool:
    """Функция проверки наличия интернета
    Проверка происходит по принципу GET-запроса
    на адрес google.com.

    ::Входные данные:
        * None
    ::Выходные данные:
        * bool - значение, равное True, если Интернет не подключен, иначе False
    """

    try:
        response = urlopen("https://www.google.ru/", timeout=5)
        return True
    except URLError:
        return False


def schedule_internet():
    """Функция проверки интернета на заднем фоне"""
    print("Запуск 5-ти минутной проверки интернета")

    response = check_internet()
    while response is False:
        time.sleep(60)
        print(False)
        response = check_internet()
    return True


if __name__ == "__main__":
    print("Проверка интернета:")
    if check_internet() != True:
        threading.Thread(target=schedule_internet).start()