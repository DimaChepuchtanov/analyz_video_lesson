from fastapi.routing import APIRouter
from fastapi import Depends, Query, HTTPException
from API.database.connect import db_conn
from API.server.depend import license_logic
from sqlalchemy.ext.asyncio import AsyncSession
from API.schemas.licenses import SchemaLicensesUpdate


license = APIRouter(tags=['lic'], prefix='/lic')


@license.get('/')
async def get_licenses(db: AsyncSession = Depends(db_conn)):
    return await license_logic.get_licences(db)


@license.post('/')
async def create_license(age: int = Query(default=365, alias='age', title='Срок лицензии в дн.'),
                         db: AsyncSession = Depends(db_conn)):

    if age < 1 or age > 365 or not age:
        return HTTPException(400, 'ошибка параметра age')
    return await license_logic.create_licence(db, age)


@license.delete('/')
async def delete_license(db: AsyncSession = Depends(db_conn),
                         id: int = Query(alias='id', title='ИН лицензии')):

    return await license_logic.delete_licence(db, id)


@license.get('/is_active')
async def is_active_license(db: AsyncSession = Depends(db_conn),
                            id: int = Query(alias='id', title='ИН лицензии')):

    return await license_logic.get_age(db, id)


@license.patch('/')
async def update_license(db: AsyncSession = Depends(db_conn),
                         license: SchemaLicensesUpdate = Depends(SchemaLicensesUpdate.verification_age)):

    return await license_logic.update_license(db, license)
