from .connect import conn
from psycopg2.extensions import cursor as cur
from typing import Optional


@conn
def insert_new_user(cursor: Optional[cur] = None,
                    data_dict: Optional[dict] = {},
                    *args,
                    **kwargs) -> dict:
    "Запись нового юзера по id"

    if type(cursor) is not cur or cursor is None:
        return {"status_code": 400,
                "title": "Ошибка входных данных",
                "discribe": "Значение 'cursor' не соответствует положенному типу данных"}

    try:
        cursor.execute("SELECT MAX(id) FROM account")
        data = cursor.fetchone()
    except Exception as e:
        return {"status_code": 510, "title": "Ошибка получения ключа", "discribe": e}

    max_id = 0 if data is None else int(data[0]) + 1

    sql = f"""INSERT INTO account VALUES(
                                        {max_id},
                                        '{data_dict["name"]}',
                                        '{data_dict["licen"]}',
                                        {data_dict["age"]},
                                        '{data_dict["company"]}',
                                        '{data_dict["login"]}',
                                        '{data_dict["password"]}'
                                        )"""

    try:
        cursor.execute(sql)
    except Exception as e:
        return {"status_code": 510, "title": "Ошибка записи", "discribe": e}
    return {"status_code": 200, "title": "Успешно", "discribe": None}


@conn
def insert_new_task(cursor: Optional[cur] = None,
                    data: Optional[dict] = {},
                    *args,
                    **kwargs) -> dict:
    "Запись нового юзера по id"

    if type(cursor) is not cur or cursor is None:
        return {"status_code": 400,
                "title": "Ошибка входных данных",
                "discribe": "Значение 'cursor' не соответствует положенному типу данных"}

    try:
        cursor.execute("SELECT MAX(id) FROM task")
        id = cursor.fetchone()
    except Exception as e:
        return {"status_code": 510, "title": "Ошибка получения ключа", "discribe": e}

    max_id = 0 if id[0] is None else int(id[0]) + 1

    try:
        cursor.execute(f"SELECT id FROM account WHERE id = {data['uid']}")
        id = cursor.fetchone()
    except Exception as e:
        return {"status_code": 510, "title": "Ошибка получения ключа пользователя", "discribe": e}

    if id is None:
        return {"status_code": 404, "title": "Пользователь не найден", "discribe": None}

    sql = f"""INSERT INTO task VALUES({max_id}, {data['uid']}, {data['mark']}, '{data["date_recog"]}', {data['duration']}, '{data["topic"]}', '{data["recommendation"]}')"""                             

    try:
        cursor.execute(sql)
    except Exception as e:
        return {"status_code": 510, "title": "Ошибка записи", "discribe": e}
    return {"status_code": 200, "title": "Успешно", "discribe": None}