from sqlalchemy.ext.asyncio import AsyncSession
from API.database.model import Company
from sqlalchemy.future import select
from API.schemas.company import SchemaCompany


class DataBaseCompany:
    async def create_company(self, db: AsyncSession, company: SchemaCompany) -> bool:
        new_company = Company(name=company.name,
                              director=company.director,
                              phone=company.phone,
                              license=company.license)

        db.add(new_company)
        try:
            await db.commit()
        except: 
            return False
        return True

    async def delete_company(self, db: AsyncSession, company_id: int) -> dict:
        company = await db.execute(select(Company).where(Company.id == company_id))
        company = company.scalars().first()

        if not company:
            return {"status": False, "exception": "CompanyNotFoud", "code": 404}

        await db.delete(company)
        await db.commit()

        return {"status": True, "exception": None, "code": 200}

    async def get_companyes(self, db: AsyncSession) -> list:
        companyes = await db.execute(select(Company))
        return companyes.scalars().all()
