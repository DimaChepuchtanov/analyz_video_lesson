from pydantic import BaseModel
import re


class SchemaCompany(BaseModel):
    name: str
    director: str
    phone: str
    license: int