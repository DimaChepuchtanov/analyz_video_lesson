from fastapi.routing import APIRouter
from fastapi import (Depends, Query,
                     Response, HTTPException,
                     Request)
from API.database.connect import db_conn
from API.server.depend import user_logic, token_logic
from sqlalchemy.ext.asyncio import AsyncSession
from API.schemas.user import SchemaUser, SchemaUserVerification
from dotmap import DotMap


ROUTE_ACCESS = {'super': ['all'],
                'admin': ['create_user', 'delete_user',
                          'get_user', 'get_user_company'],
                'user': ['get_user', 'get_user_company']}

user = APIRouter(tags=['user'], prefix='/user')


async def current_token(token: str,
                        request: Request,
                        db: AsyncSession = Depends(db_conn)):
    func = request.scope.get('route').name

    token_ = await token_logic.get_token(db, token)
    if not token_:
        raise HTTPException(403, 'TokenInvalid')

    token_lvl = await token_logic.get_token_lvl(db, token)
    if func not in ROUTE_ACCESS[token_lvl] and 'all' not in ROUTE_ACCESS[token_lvl]:
        raise HTTPException(403, 'NotAccessToken')


@user.get('/')
async def get_user(db: AsyncSession = Depends(db_conn),
                   id: int = Query(default=0, alias='id'),
                   token: str = Depends(current_token)):

    return await user_logic.get_user(db, int(id))


@user.get('/company')
async def get_user_company(db: AsyncSession = Depends(db_conn),
                           token: str = Depends(current_token),
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
                      token: str = Depends(current_token),
                      db: AsyncSession = Depends(db_conn)):

    token_ = dict(await token_logic.create_token(db))
    token_id = token_.get('token_id', None)

    if not token_id:
        raise HTTPException(510, 'Error create token')

    create = DotMap(await user_logic.create_user(db, user, token=token_id))
    if not create.status:
        return HTTPException(404, create.exception)
    else:
        return {"token": token_.get('token', None)}


@user.delete('/')
async def delete_user(db: AsyncSession = Depends(db_conn),
                      token: str = Depends(current_token),
                      id: int = Query(default=0, alias='id')):

    return await user_logic.delete_user(db, int(id))