from fastapi.routing import APIRouter
from fastapi import Depends, Query, Response
from API.database.connect import db_conn
from API.server.depend import user_logic
from sqlalchemy.ext.asyncio import AsyncSession
from API.schemas.user import SchemaUser, SchemaUserVerification
from dotmap import DotMap


user = APIRouter(tags=['user'], prefix='/user')


@user.get('/')
async def get_user(db: AsyncSession = Depends(db_conn),
                   id: int = Query(default=0, alias='id')):

    return await user_logic.get_user(db, int(id))


@user.get('/compant')
async def get_user_company(db: AsyncSession = Depends(db_conn),
                           id: int = Query(default=0, alias='id')):

    return await user_logic.get_company(db, int(id))


@user.post('/verification')
async def verification_user(user: SchemaUserVerification,
                            db: AsyncSession = Depends(db_conn)):

    result = DotMap(await user_logic.verification(db=db, user=user))
    if result.status_code == 404:
        return Response('Пользователь не найден', 404)
    elif result.status_code == 400:
        return Response(result.text, 400)
    else:
        return Response(str(result.text), 200)

@user.post('/')
async def create_user(user: SchemaUser,
                      db: AsyncSession = Depends(db_conn)):

    return await user_logic.create_user(db, user)


@user.delete('/')
async def delete_user(db: AsyncSession = Depends(db_conn),
                      id: int = Query(default=0, alias='id')):

    return await user_logic.delete_user(db, int(id))