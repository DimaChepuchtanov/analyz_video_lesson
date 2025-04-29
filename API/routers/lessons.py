from fastapi.routing import APIRouter
from fastapi import Depends, Query, HTTPException, Response
from API.database.connect import db_conn
from API.server.depend import lesson_logic
from sqlalchemy.ext.asyncio import AsyncSession
from API.schemas.lessons import SchemaLesson, SchemaLessonUpdate, SchemaAnalyz, SchemaAnalyzUpdate
from dotmap import DotMap


lesson = APIRouter(tags=['lesson'], prefix='/lesson')
analyz = APIRouter(tags=['analyz'], prefix='/analyz')


@lesson.get('/')
async def get_lessons(db: AsyncSession = Depends(db_conn)):
    return await lesson_logic.all_lesson(db)


@lesson.post('/')
async def create_lesson(new_les: SchemaLesson,
                        db: AsyncSession = Depends(db_conn)):

    return await lesson_logic.new_lesson(db, new_les)


@lesson.delete('/')
async def delete_lesson(db: AsyncSession = Depends(db_conn),
                        id: int = Query(alias='id', title='ИН урока')):

    return await lesson_logic.delete_lesson(db, id)


@lesson.delete('/')
async def delete_lessons_user(db: AsyncSession = Depends(db_conn),
                              id: int = Query(alias='id', title='ИН Пользователя')):

    return await lesson_logic.delete_all_lesson_for_user(db, id)


@lesson.patch('/')
async def update_lesson(db: AsyncSession = Depends(db_conn),
                        lesson: SchemaLessonUpdate = Depends(SchemaLessonUpdate.check_mark)):

    return await lesson_logic.update_mark(db, lesson)


@analyz.post('/')
async def create_analyz(new_analyz: SchemaAnalyz,
                        db: AsyncSession = Depends(db_conn)):

    result = await lesson_logic.new_analyz(db, new_analyz)

    return result.id


@analyz.get('/mark')
async def get_analyz_mark(id: int = Query(alias='id'),
                          db: AsyncSession = Depends(db_conn)):

    result = await lesson_logic.get_mark(db, id)

    return result


@analyz.delete('/')
async def delete_analyz(id: int = Query(alias='id', title='ИН записи анализа'),
                        db: AsyncSession = Depends(db_conn)):

    result = DotMap(await lesson_logic.delete_old_analyz(db, id))

    if result.status_code != 200:
        return HTTPException(status_code=result.status_code, detail=result.exception)
    else:
        return Response(content=result.exception, status_code=200)


@analyz.patch('/')
async def update_analyz(data: SchemaAnalyzUpdate,
                        db: AsyncSession = Depends(db_conn)):

    if data.video == '':
        data.video = None
    if data.audio == '':
        data.audio = None

    result = DotMap(await lesson_logic.update_data_analyz(db, data))

    if result.status_code != 200:
        return HTTPException(status_code=result.status_code, detail=result.exception)
    else:
        return Response(content=result.exception, status_code=200)
