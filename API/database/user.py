from API.schemas.user import SchemaUser
from sqlalchemy.ext.asyncio import AsyncSession
from API.database.model import User
from sqlalchemy.future import select


class DataBaseUser:
    async def get_user(self, db: AsyncSession, uid: int) -> dict:
        user = await db.execute(select(User).where(User.id == uid))
        user = user.scalars().first()

        if not user:
            return {"status": False, "exception": "UserNotFoud", "code": 404}
        return user

    async def get_user_password(self, db: AsyncSession, login: str) -> str:
        user = await db.execute(select(User).where(User.login == login))
        password = user.scalars().first()

        if not password:
            return "UserNotFoud"
        return password.id, password.password

    async def create_user(self, db: AsyncSession, user: SchemaUser) -> bool:
        new_user = User(name=user.name,
                        company=user.company,
                        login=user.login,
                        password=user.password,
                        role=user.role)

        db.add(new_user)
        await db.commit()
        return True

    async def delete_user(self, db: AsyncSession, uid: int) -> dict:
        user = await self.get_user(db, uid)
        if not user['status']:
            return user

        await db.delete(user)
        await db.commit()

        return {"status": True, "exception": None, "code": 200}