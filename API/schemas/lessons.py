from pydantic import BaseModel
from fastapi import HTTPException


class SchemaAnalyz(BaseModel):
    lid: int = 0
    audio: str
    video: str


class SchemaAnalyzUpdate(SchemaAnalyz):
    id: int


class SchemaLesson(BaseModel):
    uid: int
    name: str
    file: int


class SchemaLessonUpdate(BaseModel):
    id: int
    mark: int

    @staticmethod
    def check_mark(id, mark):
        if int(mark) < 0:
            return HTTPException(401, 'Оценка не может быть меньше 0')
        elif int(mark) > 100:
            return HTTPException(402, 'Оценка не может больше 100')
        else:
            return SchemaLessonUpdate(int(id), int(mark))
