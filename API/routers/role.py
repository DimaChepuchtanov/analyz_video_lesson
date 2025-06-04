from fastapi.routing import APIRouter
from fastapi import (Depends, Query,
                     HTTPException, Request)
from API.database.connect import db_conn
from API.server.depend import role_logic, token_logic
from sqlalchemy.ext.asyncio import AsyncSession


ROUTE_ACCESS = {'super': ['all'],
                'admin': ['all'],
                'user': []}


role = APIRouter(tags=['role'], prefix='/role')


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


@role.get('/')
async def get_roles(db: AsyncSession = Depends(db_conn)):
    return await role_logic.get_roles(db)


@role.post('/')
async def create_user(role_name: str = Query(alias='role'),
                      token: str = Depends(current_token),
                      db: AsyncSession = Depends(db_conn)):

    return await role_logic.create_role(db, role_name)


@role.delete('/')
async def delete_user(db: AsyncSession = Depends(db_conn),
                      token: str = Depends(current_token),
                      role_name: str = Query(alias='role')):

    return await role_logic.delete_role(db, role_name)