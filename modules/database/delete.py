from .connect import conn
from psycopg2.extensions import cursor as cur
from typing import Optional


@conn
def delete_account(cursor: Optional[cur] = None,
                   id: Optional[int] = None,
                   *args,
                   **kwargs) -> dict:
    """Удаление записи"""

    if type(cursor) is not cur or cursor is None:
        return {"status_code": 400,
                "title": "Ошибка входных данных",
                "discribe": "Значение 'cursor' не соответствует положенному типу данных"}

    try:
        cursor.execute(f"SELECT id FROM account WHERE id = {id}")
        data = cursor.fetchone()
    except Exception as e:
        return {"status_code": 510, "title": "Ошибка получения ключа", "discribe": e}

    if data is None:
        return {"status_code": 404, "title": "Пользователь не найден", "discribe": None}

    sql = f"DELETE FROM account WHERE id = {id}"

    try:
        cursor.execute(sql)
    except Exception as e:
        return {"status_code": 510, "title": "Ошибка удаления", "discribe": e}

    return {"status_code": 200, "title": "Успешно", "discribe": None}


@conn
def delete_task(cursor: Optional[cur] = None,
                   id: Optional[int] = None,
                   *args,
                   **kwargs) -> dict:
    """Удаление записи"""

    if type(cursor) is not cur or cursor is None:
        return {"status_code": 400,
                "title": "Ошибка входных данных",
                "discribe": "Значение 'cursor' не соответствует положенному типу данных"}

    try:
        cursor.execute(f"SELECT id FROM task WHERE id = {id}")
        data = cursor.fetchone()
    except Exception as e:
        return {"status_code": 510, "title": "Ошибка получения ключа", "discribe": e}

    if data is None:
        return {"status_code": 404, "title": "Пользователь не найден", "discribe": None}

    sql = f"DELETE FROM task WHERE id = {id}"

    try:
        cursor.execute(sql)
    except Exception as e:
        return {"status_code": 510, "title": "Ошибка удаления", "discribe": e}

    return {"status_code": 200, "title": "Успешно", "discribe": None}