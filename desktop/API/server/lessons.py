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
                       Каждый источник имеет стартовую позицию - время, которое отделено от остальных данных через ;
                       Тебе нужно соспоставить время для аудио данных и видео данных и оценить качество проведенного занятия
                       основываясь на вовлеченности пользователей и их эмоции.

                       Видео поток обозначается тегом Video и данные начинаются со следующего символа. Также и с тегом Audio.
                       В данных может быть фраза FaceNotFound или AudioNotFound это означает, что за данный промежуток времени
                       небыло найдено данных и тебе необходимо выставлять оценку основываясь только на известных данных.
                       Если за  нет ни аудио данных ни видео данных, ты должен сказать слово 'No'

                       Видео поток имеет структуру: время;пользователь;процент взгляда на экран;эмоция
                       Аудио поток имеет структуру: время;пользователь;сообщение;эмоция

                       Результат должен быть в формате одного единственного целого числа - оценка вовлеченности без пояснения!
                       При наличии данных, необходимо выставить оценку"""
        self.client = Client("Qwen/Qwen2.5-72B-Instruct")

    async def __gettime(self, time: datetime) -> str:
        if time == '': return ''
        time = time.split('.')[0]
        end_ = datetime.strptime(time, "%H:%M:%S")
        end_time = datetime.strftime(end_, "%H:%M:%S")
        start_time = datetime.strftime(end_ - timedelta(minutes=1), "%H:%M:%S")  # Запись 1 минута
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

    async def all_lesson(self, db: AsyncSession) -> list:
        return await self.database.get_lessons(db)

    async def current_lesson(self, db: AsyncSession, id: int) -> dict:
        return await self.database.get_lesson(db, id)

    async def new_analyz(self, db: AsyncSession, analyz: SchemaAnalyz) -> bool:
        return await self.database.create_analyz(db, analyz)

    async def delete_old_analyz(self, db: AsyncSession, id: int) -> bool:
        return await self.database.delete_analyz(db, id)

    async def update_data_analyz(self, db: AsyncSession, analyz: SchemaAnalyzUpdate) -> dict:

        #  Приведение данных к формату анализа
        #  inputVideo=>time ; user in format i start ziro ; eyes position ; emotion or FaceNotFound
        #  video=>datetime;user;eyes;emotion

        #  inputAudio=>time ; user in format i start ziro ; message ; emotion or AudioNotFound
        #  audio=>datetime;user;message;emotion

        if analyz.audio is not None:
            temp_data = ''
            for i in analyz.audio.split('\n')[:-1]:
                list_audio_data = i.split(' ; ')

                time = await self.__gettime(list_audio_data[0])

                if 'AudioNotFound' in i:
                    temp_data += f'{time};AudioNotFound'
                    continue

                user = list_audio_data[1] + 1
                message = list_audio_data[2]
                try:
                    emotion = list_audio_data[3]['dominant_emotion']
                except:
                    emotion = "Не определена"

                temp_data += f'{time};{user};{message};{emotion}\n'
            analyz.audio = temp_data

        if analyz.video is not None:
            temp_data = ''
            for i in analyz.video.split('\n')[:-1]:
                list_video_data = i.split(' ; ')

                time = await self.__gettime(list_video_data[0])

                if 'FaceNotFound' in i:
                    temp_data += f'{time};FaceNotFound'
                    continue

                user = int(list_video_data[1]) + 1
                eyes = max(0, min(1, float(list_video_data[2]))) * 100
                try:
                    emotion = list_video_data[3]
                except:
                    emotion = "Не определена"

                temp_data += f'{time};{user};{eyes};{emotion}\n'
            analyz.video = temp_data

        result = DotMap(await self.database.update_analyz(db, analyz))
        return {"status_code": result.code, "exception": result.exception}

    async def get_mark(self, db: AsyncSession, id: int) -> bool:
        data = await self.database.get_analyz(db, id)

        video = data.video.split('\n')[1:]
        audio = data.audio.split('\n')[1:]

        if len(video) > 0:
            result = self.client.predict(query=f"Video\n{video}\n\nAudio\n{audio}",
                                         history=[],
                                         system=self.text,
                                         api_name="/model_chat")
            try:
                return result[1][0][1]
            except Exception as e:
                return result[1][0][1]
