from sqlalchemy.ext.asyncio import AsyncSession
from API.database.model import Company
from sqlalchemy.future import select
from API.schemas.company import SchemaCompany
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


class DataBaseCompany:
    async def get_company(self, db: AsyncSession, id: int) -> Company:
        """_summary_

        Args:
            db (AsyncSession): _description_
            id (int): _description_

        Returns:
            Company: _description_
        """
        company = await db.execute(select(Company).where(Company.id == id))
        company = company.scalars().first()
        return company

    async def create_company(self, db: AsyncSession,
                             company: SchemaCompany) -> dict:
        """_summary_

        Args:
            db (AsyncSession): _description_
            company (SchemaCompany): _description_

        Returns:
            dict: _description_
        """
        new_company = Company(name=company.name,
                              director=company.director,
                              phone=company.phone,
                              license=company.license)

        db.add(new_company)
        try:
            await db.commit()
        except IntegrityError:
            return {"status": False,
                    "exception": "NotFoundLicense",
                    "code": 510}
        except SQLAlchemyError:
            return {"status": False,
                    "exception": "BadTransaction",
                    "code": 510}

        return {"status": True,
                "exception": None,
                "code": 200}

    async def delete_company(self, db: AsyncSession, company_id: int) -> dict:
        """_summary_

        Args:
            db (AsyncSession): _description_
            company_id (int): _description_

        Returns:
            dict: _description_
        """
        company = await self.get_company(db, company_id)

        if not company:
            return {"status": False,
                    "exception": "CompanyNotFoud",
                    "code": 404}

        try:
            await db.delete(company)
            await db.commit()
        except SQLAlchemyError:
            return {"status": False,
                    "exception": "BadTransaction",
                    "code": 510}

        return {"status": True,
                "exception": None,
                "code": 200}

    async def get_companyes(self, db: AsyncSession) -> list[Company]:
        """_summary_

        Args:
            db (AsyncSession): _description_

        Returns:
            list[Company]: _description_
        """
        companyes = await db.execute(select(Company))
        return companyes.scalars().all()
