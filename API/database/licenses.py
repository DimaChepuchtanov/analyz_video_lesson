from sqlalchemy.ext.asyncio import AsyncSession
from API.database.model import Licences
from sqlalchemy.future import select
from API.schemas.licenses import SchemaLicensesUpdate


class DataBaseLicences:
    async def create_licence(self, db: AsyncSession, age: int) -> bool:
        new_licence = Licences(age=age)

        db.add(new_licence)
        await db.commit()

        return True

    async def get_license(self, db: AsyncSession, id: int):
        licence = await db.execute(select(Licences).where(Licences.id == id))
        licence = licence.scalars().first()

        if not licence:
            return {"status": False, "exception": "LicenceNotFoud", "code": 404}

        return licence

    async def delete_licence(self, db: AsyncSession, licence_id: int) -> dict:
        license = await self.get_license(db, licence_id)
        if type(license) is dict:
            return license

        await db.delete(license)
        await db.commit()

        return {"status": True, "exception": None, "code": 200}

    async def get_licences(self, db: AsyncSession) -> list:
        licences = await db.execute(select(Licences))
        return licences.scalars().all()

    async def get_age(self, db: AsyncSession, id: int) -> list:
        age = await db.execute(select(Licences).where(Licences.id == id))
        age = age.scalars().first()

        if not age:
            return {"status": False, "exception": "LicenceNotFoud", "code": 404}

        return {"status": True, "age": age.age, "created_at": age.created_at}

    async def update_age(self, db: AsyncSession, license: SchemaLicensesUpdate):
        lic = await self.get_license(db, license.id)
        if type(lic) is dict:
            return lic

        lic.age = license.new_age

        await db.flush()
        await db.commit()
