from sqlalchemy.ext.asyncio import AsyncSession
from API.database.model import Roles
from API.database.role import DataBaseRole
from dotmap import DotMap


class MiddleLoyerRole:
    def __init__(self, database: DataBaseRole):
        self.database = database

    async def create_role(self, db: AsyncSession, role: str) -> bool:
        return await self.database.create_role(db, role)

    async def delete_role(self, db: AsyncSession, role: str) -> dict:
        result = DotMap(await self.database.delete_role(db, role))

        if result.status:
            return 'Успешно'
        else:
            return result.exception

    async def get_roles(self, db: AsyncSession) -> list:
        return await self.database.get_roles(db)
