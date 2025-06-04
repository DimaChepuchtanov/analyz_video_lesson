from sqlalchemy.ext.asyncio import AsyncSession
from API.database.model import Token
from sqlalchemy.future import select
from API.schemas.token import SchameToken
from sqlalchemy.exc import SQLAlchemyError


class DataBaseToken:
    async def get_token_with_token(self,
                                   db: AsyncSession,
                                   token: str) -> Token:
        """Получение информации о токене через
        имя токена.

        Args:
            db (AsyncSession): Асинхронная сессия к базе данных
            token (str): Токен

        Returns:
            Token: Данные токена с типом Token
        """
        token = await db.execute(select(Token).where(Token.t_name == token))
        return token.scalars().first()

    async def create_token(self,
                           db: AsyncSession,
                           token: SchameToken) -> dict:
        """Создание нового токена

        Args:
            db (AsyncSession): Асинхронная сессия к базе данных
            token (SchameToken): Токен

        Returns:
            dict: Словарь ответа
        """
        new_token = Token(t_name=token.t_name,
                          t_lvl='user')
        db.add(new_token)
        try:
            await db.commit()
        except SQLAlchemyError:
            return {"status": False,
                    "exception": "TokenDontCreate",
                    "code": 510}

        return {"status": True,
                "exception": None,
                "code": new_token.id}

    async def delete_token(self,
                           db: AsyncSession,
                           token: str) -> dict:
        """Удаление токена

        Args:
            db (AsyncSession): Асинхронная сессия к базе данных
            token (SchameToken): Токен

        Returns:
            dict: Словарь ответа
        """
        token = await self.get_token_with_token(db, token)
        if not token:
            return {"status": False,
                    "exception": "TokenNotFound",
                    "code": 404}

        try:
            await db.delete(token)
            await db.commit()
        except SQLAlchemyError:
            return {"status": False,
                    "exception": "TokenDontDelete",
                    "code": 510}

        return {"status": True,
                "exception": None,
                "code": 200}
