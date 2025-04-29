from .connect import conn
from psycopg2.extensions import cursor as cur
from typing import Optional
from datetime import datetime, timedelta


@conn
def select_user_information(cursor: Optional[cur] = None,
                            uid: Optional[int] = 0,
                            *args,
                            **kwargs) -> dict:
    """Получение данных пользователя по id"""

    if type(cursor) is not cur or cursor is None:
        return {"status_code": 400,
                "title": "Ошибка входных данных",
                "discribe": "Значение 'cursor' не соответствует положенному типу данных"}

    sql = f"SELECT name, licen, age, company FROM account WHERE id={uid}"

    try:
        cursor.execute(sql)
        data = cursor.fetchone()
    except Exception as e:
        return {"status_code": 510, "title": "Неизвестная ошибка", "discribe": e}

    if data is None:
        return {"status_code": 404, "title": "Пользователь не найден", "discribe": None}

    lic = datetime.strptime(data[1], "%Y-%m-%d %H:%M:%S")
    age = int(data[2])
    end_lic = lic + timedelta(days=age)

    result = {"name": str(data[0]),
              "company": str(data[3]),
              "start_lic": str(data[1]),
              "age_lic": int(data[2]),
              "end_lic": str(datetime.strftime(end_lic, "%Y-%m-%d %H:%M:%S"))}

    return {"status_code": 200, "title": "Успешно", "discribe": result}


@conn
def select_auth(cursor: Optional[cur] = None,
                data: Optional[dict] = {},
                *args,
                **kwargs) -> dict:
    """Проверка регистрационных данных"""

    if type(cursor) is not cur or cursor is None:
        return {"status_code": 400,
                "title": "Ошибка входных данных",
                "discribe": "Значение 'cursor' не соответствует положенному типу данных"}

    sql = f"SELECT password FROM account WHERE login='{data['login']}'"

    try:
        cursor.execute(sql)
        data = cursor.fetchone()
    except Exception as e:
        return {"status_code": 510, "title": "Неизвестная ошибка", "discribe": e}

    if data is None:
        return {"status_code": 404, "title": "Пользователь не найден", "discribe": None}

    return {"status_code": 200, "title": "Успешно", "discribe": data[0]}


@conn
def select_task_information(cursor: Optional[cur] = None,
                            id: Optional[int] = 0,
                            *args,
                            **kwargs) -> dict:
    """Получение данных пользователя по id"""

    if type(cursor) is not cur or cursor is None:
        return {"status_code": 400,
                "title": "Ошибка входных данных",
                "discribe": "Значение 'cursor' не соответствует положенному типу данных"}

    sql = f"SELECT mark, date_recog, duration, topic, recommendation FROM task WHERE id={id}"

    try:
        cursor.execute(sql)
        data = cursor.fetchone()
    except Exception as e:
        return {"status_code": 510, "title": "Неизвестная ошибка", "discribe": e}

    if data is None:
        return {"status_code": 404, "title": "Запись не найдена", "discribe": None}

    result = {"mark": int(data[0]),
              "data_recog": str(datetime.strptime(data[1], "%Y-%m-%d %H:%M:%S")),
              "duration": float(data[2]),
              "topic": str(data[3]),
              "recommendation": str(data[4])}

    return {"status_code": 200, "title": "Успешно", "discribe": result}
