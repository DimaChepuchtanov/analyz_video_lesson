import psycopg2


def conn(func):

    def wrapper(*args, **kwargs):
        try:
            database = psycopg2.connect(database='vkr',
                                        user='postgres',
                                        password='1q2w3e4r',
                                        host='localhost',
                                        port='5432')
        except Exception as e:
            print(e)
            return {"status_code": 400, "title": "Error", "discribe": e}

        result = func(database.cursor(), *args, **kwargs)
        database.commit()
        database.close()

        return result
    return wrapper

