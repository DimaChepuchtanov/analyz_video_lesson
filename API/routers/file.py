from fastapi.routing import APIRouter
from fastapi import Depends, Request, HTTPException
from API.database.connect import db_conn
from API.server.depend import file_logic, token_logic
from sqlalchemy.ext.asyncio import AsyncSession
from API.schemas.file import SchemaFile


ROUTE_ACCESS = {'super': ['all'],
                'admin': [],
                'user': ['all']}


file = APIRouter(tags=['file'], prefix='/file')


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


@file.post('/')
async def create_user(new_file: SchemaFile,
                      db: AsyncSession = Depends(db_conn)):

    return await file_logic.new_file(db, new_file)


# @role.delete('/')
# async def delete_user(db: AsyncSession = Depends(db_conn),
#                       role_name: str = Query(alias='role')):

#     return await role_logic.delete_role(db, role_name)