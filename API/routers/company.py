from fastapi.routing import APIRouter
from fastapi import Depends, Query, Request, HTTPException
from API.database.connect import db_conn
from API.server.depend import company_logic, token_logic
from sqlalchemy.ext.asyncio import AsyncSession
from API.schemas.company import SchemaCompany


ROUTE_ACCESS = {'super': ['all'],
                'admin': ['get_company', 'create_company',
                          'delete_company'],
                'user': []}


company = APIRouter(tags=['company'], prefix='/company')


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


@company.get('/')
async def get_company(db: AsyncSession = Depends(db_conn)):
    return await company_logic.get_companyes(db)


@company.post('/')
async def create_company(new_company: SchemaCompany,
                         token: str = Depends(current_token),
                         db: AsyncSession = Depends(db_conn)):
    return await company_logic.create_company(db, new_company)


@company.delete('/')
async def delete_company(db: AsyncSession = Depends(db_conn),
                         token: str = Depends(current_token),
                         id: int = Query(alias='id', title='ИН компании')):

    return await company_logic.delete_company(db, id)
