from sqlalchemy.ext.asyncio import AsyncSession
from API.database.licenses import DataBaseLicences
from dotmap import DotMap
from datetime import datetime, timedelta
from API.schemas.licenses import SchemaLicensesUpdate


class MiddleLoyerLicences:
    def __init__(self, database: DataBaseLicences):
        self.database = database

    async def create_licence(self, db: AsyncSession, age: int) -> bool:
        return await self.database.create_licence(db, age)

    async def delete_licence(self, db: AsyncSession, licence_id: int) -> str:
        result = DotMap(await self.database.delete_licence(db, licence_id))

        if result.status:
            return 'Успешно'
        else:
            return result.exception

    async def get_licences(self, db: AsyncSession) -> list:
        return await self.database.get_licences(db)

    async def get_age(self, db: AsyncSession, id: int) -> dict:
        result = DotMap(await self.database.get_age(db, id))
        if result.status:
            age = int(result.age)
            created_at = result.created_at
            is_active = True if created_at + timedelta(days=age) > datetime.now() else False
            return {"status": True, "isActive": is_active}
        else:
            return {"status": False, "exception": "LicenceNotFoud", "code": 404}

    async def update_license(self, db: AsyncSession, lic: SchemaLicensesUpdate):
        return await self.database.update_age(db, lic)
