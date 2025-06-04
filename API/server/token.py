from sqlalchemy.ext.asyncio import AsyncSession
from API.database.token import DataBaseToken
from API.schemas.token import SchameToken
from dotmap import DotMap
from secrets import token_urlsafe


class MiddleLoyerToken:
    def __init__(self, database: DataBaseToken):
        self.database = database

    async def create_token(self, db: AsyncSession) -> dict:
        __token = token_urlsafe(16)
        create = await self.database.create_token(db,
                                                  SchameToken(t_name=__token))

        create_result = DotMap(create)
        if create_result.status:
            return {"token_id": create_result.code, "token": __token}
        else:
            return {"error": create_result.exception}

    async def delete_token(self, db: AsyncSession, token: str) -> dict:
        result = DotMap(await self.database.delete_token(db, token))

        if result.status:
            return {"status": True}
        else:
            return {"error": result.exception}

    async def get_token_lvl(self, db: AsyncSession, token: str) -> str:
        result = await self.database.get_token_with_token(db, token)
        if not result:
            return 'NoLvl'
        else:
            return result.t_lvl

    async def get_token(self, db: AsyncSession, token: str) -> bool:
        result = await self.database.get_token_with_token(db, token)
        if not result:
            return False
        else:
            return True
