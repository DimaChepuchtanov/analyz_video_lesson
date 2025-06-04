from sqlalchemy.ext.asyncio import AsyncSession
from API.database.lessons import DataBaseLessons
from API.schemas.lessons import SchemaLesson, SchemaLessonUpdate, SchemaAnalyz, SchemaAnalyzUpdate
from dotmap import DotMap
from datetime import datetime, timedelta
from gradio_client import Client


class MiddleLoyeLesson:
    def __init__(self, database: DataBaseLessons):
        self.database = database
        self.text = """Ты - аналитик данных. Перед тобой данные, полученные из разных источников: видео и аудио.
                       Каждый источник имеет стартовую позицию - время, которое отделено от остальных данных через \n
                       Тебе нужно соспоставить время для аудио данных и видео данных и оценить качество проведенного занятия
                       основываясь на вовлеченности пользователей и их эмоции.

                       Видео поток обозначается тегом Video и описывает данные по выявляенным пользователям, пользователь, процент взгляда на экран, эмоция.
                       Аудио поток обозначается тегом Audio и описывает текст, который говорит спикер. Спикер - это преподаватель, его вовлеченность оценивать не нужно.
                       В данных может быть фраза FaceNotFound или AudioNotFound это означает, что за данный промежуток времени
                       небыло найдено данных и тебе необходимо выставлять оценку основываясь только на известных данных.

                       Видео поток имеет структуру: время;пользователь;процент взгляда на экран;эмоция
                       Аудио поток имеет структуру: время;пользователь;сообщение;эмоция

                       Результат должен быть в формате одного единственного целого числа - оценка вовлеченности без пояснения!
                       Расчет выполнять нужно последовательно
                       При наличии данных, необходимо выставить оценку по 100 бальной шкале"""
        self.statistic = """Ты - аналитик данных. Перед тобой данные, полученные из разных источников: видео и аудио.
                            Каждый источник имеет стартовую позицию - время, которое отделено от остальных данных через \n
                            Тебе нужно соспоставить время для аудио данных и видео данных и оценить качество проведенного занятия
                            основываясь на вовлеченности пользователей и их эмоции.

                            Видео поток обозначается тегом Video и описывает данные по выявляенным пользователям, пользователь, процент взгляда на экран, эмоция.
                            Аудио поток обозначается тегом Audio и описывает текст, который говорит спикер. Спикер - это преподаватель, его вовлеченность оценивать не нужно.
                            В данных может быть фраза FaceNotFound или AudioNotFound это означает, что за данный промежуток времени
                            небыло найдено данных и тебе необходимо выставлять оценку основываясь только на известных данных.

                            Видео поток имеет структуру: время;пользователь;процент взгляда на экран;эмоция
                            Аудио поток имеет структуру: время;пользователь;сообщение;эмоция

                            Напиши по каждому пользователю краткую характеристику для каждого временного промежутка и максиамльно сжато, в одно предложение.
                            Шаблон содержимого:
                            Время (курсив)
                            Имя - статистика"""
        self.client = Client("Qwen/Qwen2.5-72B-Instruct")

    async def __gettime(self, time: datetime) -> str:
        if time == '': return ''
        time = time.split('.')[0]
        end_ = datetime.strptime(time, "%H:%M:%S")
        end_time = datetime.strftime(end_, "%H:%M:%S")
        start_time = datetime.strftime(end_ - timedelta(minutes=30), "%H:%M:%S")  # Запись 30 секунд
        return f'{start_time}--{end_time}'

    async def new_lesson(self, db: AsyncSession, lesson: SchemaLesson) -> dict:
        return await self.database.create_lesson(db, lesson)

    async def delete_all_lesson_for_user(self, db: AsyncSession, uid: int) -> dict:
        result = DotMap(await self.database.delete_lesson_for_user(db, uid))
        return {"status_code": result.code, "exception": result.exception}

    async def delete_lesson(self, db: AsyncSession, id) -> dict:
        result = DotMap(await self.database.delete_lesson(db, id))
        return {"status_code": result.code, "exception": result.exception}

    async def update_mark(self, db: AsyncSession, lesson: SchemaLessonUpdate) -> dict:
        return await self.database.update_lesson(db, lesson)

    async def all_lesson(self, db: AsyncSession, filter: str) -> list:
        result = await self.database.get_lessons(db, filter)
        result = [[x.name, x.mark, 'Просмотреть'] for x in result]
        return result

    async def current_lesson(self, db: AsyncSession, id: int) -> dict:
        return await self.database.get_lesson(db, id)

    async def new_analyz(self, db: AsyncSession, analyz: SchemaAnalyz) -> bool:
        return await self.database.create_analyz(db, analyz)

    async def delete_old_analyz(self, db: AsyncSession, id: int) -> bool:
        return await self.database.delete_analyz(db, id)

    async def update_data_analyz(self, db: AsyncSession, analyz: SchemaAnalyzUpdate) -> dict:
        result = DotMap(await self.database.update_analyz(db, analyz))
        return {"status_code": result.code, "exception": result.exception}

    async def get_mark(self, db: AsyncSession, id: int) -> bool:
        data = await self.database.get_analyz(db, id)

        video = data.video.split('\n')[1:]
        audio = data.audio.split('\n')[1:]

        if len(video) == len(audio):
            result = self.client.predict(query=f"Video\n{video}\n\nAudio\n{audio}",
                                         history=[],
                                         system=self.text,
                                         api_name="/model_chat")
            try:
                return result[1][0][1]
            except Exception as e:
                return result[1][0][1]

    async def get_statistic(self, db: AsyncSession, id: int):
        data = await self.database.get_analyz(db, id)

        video = data.video.split('\n')[1:]
        audio = data.audio.split('\n')[1:]

        if len(video) == len(audio):
            result = self.client.predict(query=f"Video\n{video}\n\nAudio\n{audio}",
                                         history=[],
                                         system=self.statistic,
                                         api_name="/model_chat")
            try:
                return result[1][0][1]
            except Exception as e:
                return result[1][0][1]
