from sqlalchemy.ext.asyncio import AsyncSession
from API.database.company import DataBaseCompany
from API.schemas.company import SchemaCompany
from dotmap import DotMap


class MiddleLoyeCompany:
    def __init__(self, database: DataBaseCompany):
        self.database = database

    async def create_company(self, db: AsyncSession, company: SchemaCompany) -> bool:

        return await self.database.create_company(db, company) 

    async def delete_company(self, db: AsyncSession, company_id: int) -> str:
        result = DotMap(await self.database.delete_company(db, company_id))

        if result.status:
            return "Успешно"
        else:
            return result.exception

    async def get_companyes(self, db: AsyncSession) -> list:
        return await self.database.get_companyes(db)
