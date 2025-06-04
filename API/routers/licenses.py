from fastapi.routing import APIRouter
from fastapi import (Depends, Query,
                     HTTPException, Request)
from API.database.connect import db_conn
from API.server.depend import license_logic, token_logic
from sqlalchemy.ext.asyncio import AsyncSession
from API.schemas.licenses import SchemaLicensesUpdate


ROUTE_ACCESS = {'super': ['all'],
                'admin': ['all'],
                'user': []}

license = APIRouter(tags=['lic'], prefix='/lic')


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


@license.get('/')
async def get_licenses(db: AsyncSession = Depends(db_conn)):
    return await license_logic.get_licences(db)


@license.post('/')
async def create_license(age: int = Query(default=365, alias='age', title='Срок лицензии в дн.'),
                         token: str = Depends(current_token),
                         db: AsyncSession = Depends(db_conn)):

    if age < 1 or age > 365 or not age:
        return HTTPException(400, 'ошибка параметра age')
    return await license_logic.create_licence(db, age)


@license.delete('/')
async def delete_license(db: AsyncSession = Depends(db_conn),
                         token: str = Depends(current_token),
                         id: int = Query(alias='id', title='ИН лицензии')):

    return await license_logic.delete_licence(db, id)


@license.get('/is_active')
async def is_active_license(db: AsyncSession = Depends(db_conn),
                            token: str = Depends(current_token),
                            id: int = Query(alias='id', title='ИН лицензии')):

    return await license_logic.get_age(db, id)


@license.patch('/')
async def update_license(db: AsyncSession = Depends(db_conn),
                         token: str = Depends(current_token),
                         license: SchemaLicensesUpdate = Depends(SchemaLicensesUpdate.verification_age)):

    return await license_logic.update_license(db, license)
