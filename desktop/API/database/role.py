from sqlalchemy.ext.asyncio import AsyncSession
from API.database.model import Roles
from sqlalchemy.future import select


class DataBaseRole:
    async def create_role(self, db: AsyncSession, role: str) -> bool:
        new_role = Roles(title=role)

        db.add(new_role)
        await db.commit()
        return True

    async def delete_role(self, db: AsyncSession, role: str) -> dict:
        role = await db.execute(select(Roles).where(Roles.title == role))
        role = role.scalars().first()

        if not role:
            return {"status": False, "exception": "RoleNotFoud", "code": 404}

        await db.delete(role)
        await db.commit()

        return {"status": True, "exception": None, "code": 200}

    async def get_roles(self, db: AsyncSession) -> list:
        roles = await db.execute(select(Roles))
        return roles.scalars().all()
