from sqlalchemy.ext.asyncio import AsyncSession
from API.database.model import Lessons, VideoAudioAnalyz
from sqlalchemy.future import select
from sqlalchemy import delete
from API.schemas.lessons import (SchemaLesson,
                                 SchemaLessonUpdate,
                                 SchemaAnalyz,
                                 SchemaAnalyzUpdate)


class DataBaseLessons:
    async def create_lesson(self, db: AsyncSession, lesson: SchemaLesson) -> bool:
        new_lesson = Lessons(uid=lesson.uid,
                             name=lesson.name,
                             file=lesson.file)

        db.add(new_lesson)
        await db.commit()
        return new_lesson

    async def delete_lesson(self, db: AsyncSession, id: int) -> dict:
        lesson = await self.get_lesson(db, id)
        if not lesson:
            return {"status": False, "exception": "LessonNotFound", "code": 404}

        await db.delete(lesson)
        await db.commit()
        return {"status": True, "exception": None, "code": 200}

    async def delete_lesson_for_user(self, db: AsyncSession, uid: int) -> dict:
        lessons = await db.execute(select(Lessons).where(Lessons.uid == uid))
        lessons = lessons.scalars().all()

        if not lessons:
            return {"status": False, "exception": "LessonsForUserNotFound", "code": 404}

        await db.execute(delete(Lessons).where(Lessons.uid == uid).execution_options(synchronize_session=False))
        await db.commit()

        return {"status": True, "exception": None, "code": 200}

    async def get_lessons(self, db: AsyncSession) -> list:
        roles = await db.execute(select(Lessons))
        return roles.scalars().all()

    async def get_lesson(self, db: AsyncSession, id: int) -> Lessons:
        roles = await db.execute(select(Lessons).where(Lessons.id == id))
        return roles.scalars().first()

    async def update_lesson(self, db: AsyncSession, task: SchemaLessonUpdate):
        lesson = await self.get_lesson(db, task.id)
        if not lesson:
            return {"status": False, "exception": "LessonNotFound", "code": 404}

        lesson.mark = task.mark
        await db.flush()
        await db.commit()

        return {"status": True, "exception": None, "code": 200}

    async def get_analyz(self,  db: AsyncSession, id: int) -> VideoAudioAnalyz:
        data_analyz = await db.execute(select(VideoAudioAnalyz).where(VideoAudioAnalyz.id == id))
        return data_analyz.scalars().first()

    async def create_analyz(self, db: AsyncSession, data: SchemaAnalyz) -> bool:
        new_analyz = VideoAudioAnalyz(lid=data.lid,
                                      video=data.video,
                                      audio=data.audio)

        db.add(new_analyz)
        await db.commit()
        return new_analyz

    async def update_analyz(self, db: AsyncSession, analyz: SchemaAnalyzUpdate) -> dict:
        data_analyz = await self.get_analyz(db, analyz.id)
        if not data_analyz:
            return {"status": False, "exception": "AnalyzNotFound", "code": 404}

        data_analyz.video = data_analyz.video + "\n" + analyz.video if analyz.video is not None else data_analyz.video
        data_analyz.audio = data_analyz.audio + "\n" + analyz.audio if analyz.audio is not None else data_analyz.audio

        await db.flush()
        await db.commit()

        return {"status": True, "exception": None, "code": 200}

    async def delete_analyz(self, db: AsyncSession, id: int) -> bool:
        data_analyz = await self.get_analyz(db, id)
        if not data_analyz:
            return {"status": False, "exception": "AnalyzNotFound", "code": 404}

        await db.delete(data_analyz)
        await db.commit()
        return True
