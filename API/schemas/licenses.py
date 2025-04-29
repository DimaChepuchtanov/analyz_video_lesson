from pydantic import BaseModel
from fastapi import HTTPException


class SchemaLicensesUpdate(BaseModel):
    id: int
    new_age: int

    @staticmethod
    def verification_age(id, new_age):
        if int(new_age) < 0 or int(new_age) > 365:
            raise HTTPException(400, 'Ошибка возраста лицензии')
        else:
            return SchemaLicensesUpdate(id=int(id), new_age=int(new_age))
