from pydantic import BaseModel


class SchemaUser(BaseModel):
    name: str
    company: int
    role: int
    password: str
    login: str


class SchemaUserVerification(BaseModel):
    password: str
    login: str