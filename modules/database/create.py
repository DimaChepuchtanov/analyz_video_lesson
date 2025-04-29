import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .connect import conn
from psycopg2.extensions import cursor as cur
from typing import Optional


@conn
def create_table(cursor: Optional[cur] = None):
    """Создание таблиц"""

    if type(cursor) is not cur or cursor is None:
        return {"status_code": 400,
                "title": "Ошибка входных данных",
                "discribe": "Значение 'cursor' не соответствует положенному типу данных"}

    current_create_table_list = ["account", "task"]
    create_table_list = []
    logs = ""

    # Создание таблицы account
    sql = """CREATE TABLE IF NOT EXISTS account
            (
                id INTEGER NOT NULL,
                name TEXT NOT NULL,
                company TEXT NOT NULL,
                login TEXT NOT NULL,
                password TEXT NOT NULL
            )"""

    try:
        cursor.execute(sql)
    except Exception as e:
        logs += f"account: -> {e}"
    else:
        logs += f"account: -> Успешно\n"
        create_table_list.append('account')

    # Создание таблицы account
    sql = """CREATE TABLE IF NOT EXISTS task
            (
                id INTEGER NOT NULL,
                uid INTEGER NOT NULL,
                mark INTEGER NOT NULL,
                date_recog TEXT NOT NULL,
                duration DECIMAL NOT NULL,
                topic TEXT NOT NULL,
                recommendation TEXT NOT NULL,
                url_recog TEXT
            )"""

    try:
        cursor.execute(sql)
    except Exception as e:
        logs += f"task: -> {e}"
    else:
        logs += f"task: -> Успешно"
        create_table_list.append('task')

    if current_create_table_list == create_table_list:
        return {"status_code": 200, "title": "Успешно", "discribe": "Все таблицы созданы"}
    elif len(current_create_table_list) > len(create_table_list) and len(create_table_list) > 0:
        return {"status_code": 206, "title": "Не все, см. 'discribe'", "discribe": f"Логи создания: {logs}"}
    else:
        return {"status_code": 500, "title": "Таблицы не созданы", "discribe": f"Логи: {logs}"}



if __name__ == "__main__":
    create_table()
