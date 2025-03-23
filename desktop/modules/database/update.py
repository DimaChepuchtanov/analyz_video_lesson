from .connect import conn
from psycopg2.extensions import cursor as cur
from typing import Optional


@conn
def update_user_information(cursor: Optional[cur] = None,
                            data_dict: Optional[dict] = {},
                            *args,
                            **kwargs) -> dict:
    ""

    if type(cursor) is not cur or cursor is None:
        return {"status_code": 400,
                "title": "Ошибка входных данных",
                "discribe": "Значение 'cursor' не соответствует положенному типу данных"}
    try:
        cursor.execute(f"SELECT id FROM account WHERE id = {data_dict['id']}")
        data = cursor.fetchone()
    except Exception as e:
        return {"status_code": 510, "title": "Ошибка получения ключа", "discribe": e}

    if data is None:
        return {"status_code": 404, "title": "Пользователь не найден", "discribe": None}

    sql = f"""UPDATE account SET name = '{data_dict["name"]}',
                                 age = {data_dict["age"]},
                                 company = '{data_dict["company"]}'
                                 WHERE id={data_dict["id"]};"""

    try:
        cursor.execute(sql)
    except Exception as e:
        return {"status_code": 510, "title": "Ошибка обновления записи", "discribe": e}
    return {"status_code": 200, "title": "Успешно", "discribe": None}


@conn
def update_task_information(cursor: Optional[cur] = None,
                            data_dict: Optional[dict] = {},
                            *args,
                            **kwargs) -> dict:
    ""

    if type(cursor) is not cur or cursor is None:
        return {"status_code": 400,
                "title": "Ошибка входных данных",
                "discribe": "Значение 'cursor' не соответствует положенному типу данных"}
    try:
        cursor.execute(f"SELECT id FROM task WHERE id = {data_dict['id']}")
        data = cursor.fetchone()
    except Exception as e:
        return {"status_code": 510, "title": "Ошибка получения ключа", "discribe": e}

    if data is None:
        return {"status_code": 404, "title": "Запись не найден", "discribe": None}

    sql = f"""UPDATE task SET uid = {data_dict['uid']},
                                 mark = {data_dict['mark']},
                                 date_recog = '{data_dict["date_recog"]}',
                                 duration = '{data_dict["duration"]}',
                                 topic = '{data_dict["topic"]}',
                                 recommendation = '{data_dict["recommendation"]}'
                                 WHERE id={data_dict["id"]};"""

    try:
        cursor.execute(sql)
    except Exception as e:
        return {"status_code": 510, "title": "Ошибка обновления записи", "discribe": e}
    return {"status_code": 200, "title": "Успешно", "discribe": None}