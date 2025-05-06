from pydantic import BaseModel
from fastapi import HTTPException


class SchemaFile(BaseModel):
    path: str = "None"
    duration: str = '00:00:00'
    size: str = '0 bytes'
    text_data: str = "None"