from sqlalchemy.ext.asyncio import AsyncSession
from API.database.model import FileStorage
from sqlalchemy.future import select
from API.schemas.file import SchemaFile


class DataBaseFile:
    async def create_file(self, db: AsyncSession, file: SchemaFile) -> bool:
        new_file = FileStorage(path=file.path,
                               duration=file.duration,
                               size=file.size,
                               text_data=file.text_data)

        db.add(new_file)
        await db.commit()
        return new_file

    # async def delete_role(self, db: AsyncSession, role: str) -> dict:
    #     role = await db.execute(select(Roles).where(Roles.title == role))
    #     role = role.scalars().first()

    #     if not role:
    #         return {"status": False, "exception": "RoleNotFoud", "code": 404}

    #     await db.delete(role)
    #     await db.commit()

    #     return {"status": True, "exception": None, "code": 200}

    # async def get_roles(self, db: AsyncSession) -> list:
    #     roles = await db.execute(select(Roles))
    #     return roles.scalars().all()
