import uvicorn
import os
from fastapi import FastAPI
from API.routers.user import user
from API.routers.company import company
from API.routers.licenses import license
from API.routers.lessons import lesson, analyz
from API.routers.role import role
from API.routers.file import file
from API.database.connect import engine
from API.database.model import Base


app = FastAPI()
app.include_router(user)
app.include_router(company)
app.include_router(license)
app.include_router(role)
app.include_router(analyz)
app.include_router(lesson)
app.include_router(file)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    uvicorn.run('api:app')