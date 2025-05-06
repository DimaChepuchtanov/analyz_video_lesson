from fastapi.routing import APIRouter
from fastapi import Depends, Query
from API.database.connect import db_conn
from API.server.depend import company_logic
from sqlalchemy.ext.asyncio import AsyncSession
from API.schemas.company import SchemaCompany


company = APIRouter(tags=['company'], prefix='/company')


@company.get('/')
async def get_licenses(db: AsyncSession = Depends(db_conn)):
    return await company_logic.get_companyes(db)


@company.post('/')
async def create_company(new_company: SchemaCompany,
                         db: AsyncSession = Depends(db_conn)):
    return await company_logic.create_company(db, new_company)


@company.delete('/')
async def delete_company(db: AsyncSession = Depends(db_conn),
                         id: int = Query(alias='id', title='ИН компании')):

    return await company_logic.delete_company(db, id)
