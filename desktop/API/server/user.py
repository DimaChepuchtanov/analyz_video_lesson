from API.schemas.user import SchemaUser, SchemaUserVerification
from sqlalchemy.ext.asyncio import AsyncSession
from API.database.user import DataBaseUser
from cryptography.fernet import Fernet
from API.server.setting import setting


class MiddleLoyerUser:
    def __init__(self, database: DataBaseUser):
        self.database = database

    async def __encrypt(self, string):
        '''string:str, key:str'''
        fernet = Fernet(setting.SECRET_KEY)
        return fernet.encrypt(string.encode())

    async def __decrypt(self, string):
        '''string:str, key:str'''
        fernet = Fernet(setting.SECRET_KEY)
        return fernet.decrypt(string).decode()

    async def create_user(self, db: AsyncSession, user: SchemaUser) -> bool:

        password = await self.__encrypt(user.password)
        user.password = password.decode()

        result = await self.database.create_user(db=db, user=user)
        return True

    async def delete_user(self, db: AsyncSession, uid: int) -> dict:
        return await self.database.delete_user(db, uid)

    async def verification(self, db: AsyncSession, user: SchemaUserVerification) -> dict:
        password_db = await self.database.get_user_password(db, user.login)
        if password_db == "UserNotFoud":
            return {"status_code": 404, 'text': password_db}

        decript_password = await self.__decrypt(password_db[1])
        if decript_password == user.password:
            return {"status_code": 200, 'text': password_db[0]}
        else:
            return {"status_code": 400, 'text': "Пароль не верный"}

    async def get_company(self, db: AsyncSession, uid: int) -> int:
        user = await self.database.get_user(db, uid)
        return int(user.company)

    async def get_user(self, db: AsyncSession, uid: int) -> int:
        user = await self.database.get_user(db, uid)
        return user
