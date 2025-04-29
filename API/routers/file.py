from fastapi.routing import APIRouter
from fastapi import Depends, Query
from API.database.connect import db_conn
from API.server.depend import file_logic
from sqlalchemy.ext.asyncio import AsyncSession
from API.schemas.file import SchemaFile


file = APIRouter(tags=['file'], prefix='/file')


@file.post('/')
async def create_user(new_file: SchemaFile,
                      db: AsyncSession = Depends(db_conn)):

    return await file_logic.new_file(db, new_file)


# @role.delete('/')
# async def delete_user(db: AsyncSession = Depends(db_conn),
#                       role_name: str = Query(alias='role')):

#     return await role_logic.delete_role(db, role_name)