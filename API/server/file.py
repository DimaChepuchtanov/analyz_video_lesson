from sqlalchemy.ext.asyncio import AsyncSession
from API.database.file import DataBaseFile
from dotmap import DotMap
from API.schemas.file import SchemaFile


class MiddleLoyerFile:
    def __init__(self, database: DataBaseFile):
        self.database = database

    async def new_file(self, db: AsyncSession, file: SchemaFile) -> bool:
        return await self.database.create_file(db, file)

    # async def delete_role(self, db: AsyncSession, role: str) -> dict:
    #     result = DotMap(await self.database.delete_role(db, role))

    #     if result.status:
    #         return 'Успешно'
    #     else:
    #         return result.exception

    # async def get_roles(self, db: AsyncSession) -> list:
    #     return await self.database.get_roles(db)
