import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, Response, jsonify, request
from flasgger import Swagger
from cryptography.fernet import Fernet
from datetime import datetime
from dotmap import DotMap
from setting import pwo
from database import (get_user_information,
                      get_task_information,
                      update_user_information,
                      update_task_information,
                      get_auth, create_table,
                      add_user, delete_account,
                      del_task, add_task)


def encrypt(string):
    '''string:str, key:str'''
    fernet = Fernet("UpywWKvxUSi8gpBUYS_ZUX0r_TpgY9ymjoEubeXxhU0=")
    return fernet.encrypt(string.encode())


def decrypt(string):
    '''string:str, key:str'''
    fernet = Fernet("UpywWKvxUSi8gpBUYS_ZUX0r_TpgY9ymjoEubeXxhU0=")
    return fernet.decrypt(string).decode()


# Иницилизация Swagger + внешний вид
template = {
  "swagger": "2.0",
  "info": {
    "title": "API Анализ Речи",
    "description": "API для анализа речи, включая личный кабинет",
    "contact": {
      "responsibleOrganization": "ME",
      "responsibleDeveloper": "Me",
      "email": "dmitrii.chepushtanov@r-x.team",
    },
    "version": "1.0.0"
  }
}

# Иницилизация класса Flask
app = Flask(__name__)

# Иницилизация класса Swagger
swagger = Swagger(app, template=template)


#  Блок учетной записи
# [.]_[.] ! (ДОКУМЕНТАЦИЯ!!)
@app.route('/api/v1/account/update-user', methods=['PATCH'])
def update_user():
    """Обновление данных пользователя

    Обновляются только второстепенные данные. uid НЕ МЕНЯЕТСЯ!

    ---
    tags:
      - USER
    parameters:
      - name: data
        in: body
        required: true
        schema:
          type: object
          properties:
              id:
                type: integer
                example: 0
              name:
                type: string
                example: "Алина"
              company:
                type: string
                description: Фамилия
                example: "Иванович"
              age:
                type: integer
                description: Количество дней | 365 или 183
                example: 365
    responses:
      201:
        description: Пользователь создан
      400:
        description: Некорректный запрос
      404:
        description: Не найдено
      415:
        description: Неподдерживаемый тип данных
      500:
        description: Ошибка выполнения действия со стороны бэка
      510:
        description: Неизвестная ошибка
    """
    data = dict(request.json)

    current_key = sorted(['id', 'name', 'company', 'age'])
    key_list = sorted(list(data.keys()))
    if current_key != key_list:
        return Response("Ошибка ключей", 400)

    result = DotMap(get_user_information(id=data['id']))
    if result.status_code == 510:
        return Response("Ошибка получения данных пользователя", 510)
    elif result.status_code == 404:
        return Response("Пользователь не найден", 404)

    result = DotMap(update_user_information(data_dict=data))
    if result.status_code == 510:
        return Response("Ошибка обновления", 510)
    elif result.status_code == 404:
        return Response("Пользователь не найден", 404)

    return Response("Данные обновлены", 200)


# [.]_[.] ! (ДОКУМЕНТАЦИЯ!!)
@app.route("/api/v1/account/delete-user/<id>", methods=['DELETE'])
def delete_user(id):
    """Удаление учетной записи по id

    ---
    tags:
      - USER
    parameters:
      - name: id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Пользователь удален
      400:
        description: Некорректный запрос
      404:
        description: Не найдено
      415:
        description: Неподдерживаемый тип данных
      500:
        description: Ошибка выполнения действия со стороны бэка
      510:
        description: Неизвестная ошибка
    """
    try:
        uid = int(id)
    except Exception as e:
        return Response("Ошибка получения id", 415)

    #  Задаем возможность обращения к ключу через точку
    data = DotMap(delete_account(id=uid))
    if data.status_code == 510:
        return Response('Ошибка получения данных', 510)
    elif data.status_code == 404:
        return Response('Пользователь не найден', 404)
    else:
        return Response('Запись удалена', 200)


# [.]_[.] ! (ДОКУМЕНТАЦИЯ!!)
@app.route('/api/v1/account/get-user/<id>', methods=['GET'])
def get_user(id):
    """Получение данных о пользователе по id

    ---
    tags:
      - USER
    parameters:
      - name: id
        in: path
        required: true
        type: integer
    responses:
      201:
        description: Пользователь создан
      400:
        description: Некорректный запрос
      404:
        description: Не найдено
      415:
        description: Неподдерживаемый тип данных
      500:
        description: Ошибка выполнения действия со стороны бэка
      510:
        description: Неизвестная ошибка
    """

    try:
        uid = int(id)
    except Exception as e:
        return Response("Ошибка получения id", 415)

    #  Задаем возможность обращения к ключу через точку
    data = DotMap(get_user_information(uid=uid))
    if data.status_code == 510:
        return Response('Ошибка получения данных из базы', 510)
    elif data.status_code == 404:
        return Response('Пользователь не найден', 404)
    else:
        return jsonify({"name": data.discribe.name,
                        "company": data.discribe.company,
                        'licence': data.discribe.start_lic,
                        "end_licence": data.discribe.end_lic,
                        "age": str(data.discribe.age_lic) + " дней"}), 200


#  Блок авторизации
# [.]_[.] ! (ДОКУМЕНТАЦИЯ!!)
@app.route('/api/v1/auth', methods=['POST'])
def auth():
    """Авторизация пользователя

    ---
    tags:
      - AUTH
    parameters:
      - name: data
        in: body
        required: true
        schema:
          type: object
          properties:
              login:
                type: string
                example: "wqe@mail.ru"
              password:
                type: string
                example: "Алина"
    responses:
      201:
        description: Пользователь создан
      400:
        description: Некорректный запрос
      404:
        description: Не найдено
      415:
        description: Неподдерживаемый тип данных
      500:
        description: Ошибка выполнения действия со стороны бэка
      510:
        description: Неизвестная ошибка
    """
    try:
        data = request.json
    except Exception as e:
        return Response("Не верный формат данных", 400)

    # Проверка соответствия ключей
    key = sorted(list(data.keys()))
    current_key = sorted(['login', 'password'])
    if current_key != key:
        return Response("Не верные ключи словаря", 400)

    # Проверка наличия пользователя в базе
    result = get_auth(data=data)
    if result['status_code'] == 404:
        return Response("Данные не найдены в базе", 404)

    result = result['discribe']
    if decrypt(str(result).encode()) != data['password']:
        return Response("Не верный пароль", 400)
    elif decrypt(str(result).encode()) == data['password']:
        return Response("Пароль верный", 200)
    else:
        return Response("Ошибка", 510)


# [.]_[.] ! (ДОКУМЕНТАЦИЯ!!)
@app.route('/api/v1/reg', methods=['POST'])
def reg():
    """Регистрация пользователя

    <b>Описание</b>
    &nbsp;&nbsp;&nbsp; Регистрация пользователя происходит по указанным параметрам
    Если какой-либо из параметров отсутствует, необходимо проставить `-` в качестве значения ключа.

    Пароль можно задать как пользовательский, так и системный.
    <b>Пользовательский</b> пароль задается самим пользователем.
    <b>Системный</b> пароль задается системой и после успешного сохранения возвращаются данные пользователя.

    Сейчас, в параметрах не указан ключ password — это означает, что по умолчанию пароль системный!
    Для перехода на пользовательский пароль, нужно указать ключ `password`

    Если хотите задать свой пароль, добавьте тег password.

    ---
    tags:
      - AUTH
    parameters:
      - name: data
        in: body
        required: true
        schema:
          type: object
          properties:
            login:
                type: string
                description: Логин
                example: "your@mail.ru"
            name:
                type: string
                description: Имя
                example: "Иван"
            company:
                type: string
                description: Фамилия
                example: "Иванович"
            age:
                type: integer
                description: Количество дней | 365 или 183
                example: 365
    responses:
      201:
        description: Пользователь создан
      400:
        description: Некорректный запрос
      404:
        description: Не найдено
      415:
        description: Неподдерживаемый тип данных
      500:
        description: Ошибка выполнения действия со стороны бэка
      510:
        description: Неизвестная ошибка
    """

    try:
        data = dict(request.json)
    except Exception as e:
        return Response("Не корректный запрос", 400)

    # Проверка соответствия ключей
    key = list(data.keys())
    if len(key) > 2 and "password" in key:
        new_key = sorted([x for x in key if x != "password"])
    else:
        new_key = sorted(key)
    current_key = sorted(['name', 'company', 'login', 'age'])
    if current_key != new_key:
        return Response("Не верные ключи словаря", 400)

    # Проверка соответствия почты
    if "@" not in data['login']:
        return Response("Mail указан не верно", 400)

    # Проверка наличия данных
    result = get_auth(data=data)
    if result['status_code'] == 200:
        return Response("Пользователь уже есть в системе", 400)

    # Генерация пароля
    if "password" not in key:
        key = pwo.generate()
    else:
        key = data['password']

    value = {"login": data["login"],
             "password": encrypt(key).decode(),
             "name": data['name'],
             "company": data['company'],
             "age": int(data['age']),
             "licen": str(datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"))}

    result = add_user(data_dict=value)
    if result['status_code'] == 200:
        return jsonify({"login": data['login'], "password": key})

    if result['status_code'] == 500:
        return Response("Ошибка", 510)


#  Блок работы с записями
# [.]_[.] ! (ДОКУМЕНТАЦИЯ!!)
@app.route("/api/v1/task/new-task", methods=['POST'])
def new_task():
    """Регистрация пользователя

    <b>Описание</b>
    &nbsp;&nbsp;&nbsp; Регистрация пользователя происходит по указанным параметрам
    Если какой-либо из параметров отсутствует, необходимо проставить `-` в качестве значения ключа.

    Пароль можно задать как пользовательский, так и системный.
    <b>Пользовательский</b> пароль задается самим пользователем.
    <b>Системный</b> пароль задается системой и после успешного сохранения возвращаются данные пользователя.

    Сейчас, в параметрах не указан ключ password — это означает, что по умолчанию пароль системный!
    Для перехода на пользовательский пароль, нужно указать ключ `password`

    Если хотите задать свой пароль, добавьте тег password.

    ---
    tags:
      - TASK
    parameters:
      - name: data
        in: body
        required: true
        schema:
          type: object
          properties:
            uid:
                type: INTEGER
                description: ID пользователя
                example: 1
            mark:
                type: INTEGER
                description: Оценка
                example: 15
            date_recog:
                type: string
                description: Дата записи
                example: "2024-10-10 23:00:00"
            duration:
                type: demical
                description: Длина записи
                example: 29.1
            topic:
                type: string
                description: Название темы
                example: "Тест"
            recommendation:
                type: string
                description: Рекомендации ИИ
                example: "Провести тестирование"
    responses:
      201:
        description: Пользователь создан
      400:
        description: Некорректный запрос
      404:
        description: Не найдено
      415:
        description: Неподдерживаемый тип данных
      500:
        description: Ошибка выполнения действия со стороны бэка
      510:
        description: Неизвестная ошибка
    """
    try:
        data = dict(request.json)
    except Exception as e:
        return Response("Не корректный запрос", 400)

    # Проверка соответствия ключей
    current_key = sorted(['uid', 'mark', 'date_recog', 'duration', 'topic', 'recommendation'])
    if current_key != sorted(list(data.keys())):
        return Response("Не верные ключи словаря", 400)

    result = DotMap(add_task(data=data))

    if result.status_code == 404:
        return Response("Указаный uid пользователя не найден в базе", 404)
    elif result.status_code == 510:
        return Response("Ошибка", 510)
    else:
        return Response("Успешно", 200)


# [.]_[.] ! (ДОКУМЕНТАЦИЯ!!)
@app.route("/api/v1/task/get-task/<id>", methods=['GET'])
def get_tasks(id):
    """Получение данных о записи по id

    ---
    tags:
      - TASK
    parameters:
      - name: id
        in: path
        required: true
        type: integer
    responses:
      201:
        description: Пользователь создан
      400:
        description: Некорректный запрос
      404:
        description: Не найдено
      415:
        description: Неподдерживаемый тип данных
      500:
        description: Ошибка выполнения действия со стороны бэка
      510:
        description: Неизвестная ошибка
    """
    try:
        uid = int(id)
    except Exception as e:
        return Response("Ошибка получения id", 415)

    #  Задаем возможность обращения к ключу через точку
    data = DotMap(get_task_information(id=uid))
    if data.status_code == 510:
        return Response('Ошибка получения данных', 510)
    elif data.status_code == 404:
        return Response('Запись не найден', 404)
    else:
        return jsonify(dict(data.discribe)), 200


# [.]_[.] ! (ДОКУМЕНТАЦИЯ!!)
@app.route("/api/v1/task/update-task", methods=['PATCH'])
def update_task():
    """Обновление данных пользователя

    Обновляются только второстепенные данные. uid НЕ МЕНЯЕТСЯ!

    ---
    tags:
      - TASK
    parameters:
      - name: data
        in: body
        required: true
        schema:
          type: object
          properties:
              id:
                type: INTEGER
                description: ID пользователя
                example: 1
              uid:
                type: INTEGER
                description: ID пользователя
                example: 1
              mark:
                  type: INTEGER
                  description: Оценка
                  example: 15
              date_recog:
                  type: string
                  description: Дата записи
                  example: "2024-10-10 23:00:00"
              duration:
                  type: demical
                  description: Длина записи
                  example: 29.1
              topic:
                  type: string
                  description: Название темы
                  example: "Тест"
              recommendation:
                  type: string
                  description: Рекомендации ИИ
                  example: "Провести тестирование"
    responses:
      201:
        description: Пользователь создан
      400:
        description: Некорректный запрос
      404:
        description: Не найдено
      415:
        description: Неподдерживаемый тип данных
      500:
        description: Ошибка выполнения действия со стороны бэка
      510:
        description: Неизвестная ошибка
    """
    try:
        data = dict(request.json)
    except Exception as e:
        return Response("Не корректный запрос", 400)

    # Проверка соответствия ключей
    current_key = sorted(['id', 'uid', 'mark', 'date_recog', 'duration', 'topic', 'recommendation'])
    if current_key != sorted(list(data.keys())):
        return Response("Не верные ключи словаря", 400)

    result = DotMap(update_task_information(data_dict=data))
    if result.status_code == 510:
        return Response("Ошибка обновления", 510)
    elif result.status_code == 404:
        return Response("Запись не найден", 404)
    else:
        return Response("Данные обновлены", 200)


# [.]_[.] ! (ДОКУМЕНТАЦИЯ!!)
@app.route("/api/v1/task/delete-task/<id>", methods=['DELETE'])
def delete_task(id):
    """Удаление записи по id

    ---
    tags:
      - TASK
    parameters:
      - name: id
        in: path
        required: true
        type: integer
    responses:
      201:
        description: Пользователь создан
      400:
        description: Некорректный запрос
      404:
        description: Не найдено
      415:
        description: Неподдерживаемый тип данных
      500:
        description: Ошибка выполнения действия со стороны бэка
      510:
        description: Неизвестная ошибка
    """
    try:
        uid = int(id)
    except Exception as e:
        return Response("Ошибка получения id", 415)

    result = DotMap(del_task(id=uid))
    if result.status_code == 200:
        return Response("Успешно", 200)
    elif result.status_code == 404:
        return Response("Запись не найдена", 404)
    else:
        return Response("Ошибка", 510)


if __name__ == "__main__":
    print("--::: Настройка базы данных :::--")
    result = DotMap(create_table())
    if result.status_code == 500:
        print("Ошибка создания таблиц. Завершение программы")
    elif result.status_code == 206:
        print("Одна из таблиц не создана!")
        print(result.discribe)
        app.run()
    else:
        print("--::: Настройка пройдена :::--")
        print("--::: Запуск API :::--")
        app.run()