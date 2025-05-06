from fastapi.routing import APIRouter
from fastapi import Depends, Query
from API.database.connect import db_conn
from API.server.depend import role_logic
from sqlalchemy.ext.asyncio import AsyncSession


role = APIRouter(tags=['role'], prefix='/role')


@role.get('/')
async def get_roles(db: AsyncSession = Depends(db_conn)):
    return await role_logic.get_roles(db)


@role.post('/')
async def create_user(role_name: str = Query(alias='role'),
                      db: AsyncSession = Depends(db_conn)):

    return await role_logic.create_role(db, role_name)


@role.delete('/')
async def delete_user(db: AsyncSession = Depends(db_conn),
                      role_name: str = Query(alias='role')):

    return await role_logic.delete_role(db, role_name)