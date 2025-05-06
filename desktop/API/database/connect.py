from API.server.setting import setting
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


engine = create_async_engine(f'postgresql+asyncpg://{setting.POSTGRES_USER}:{setting.POSTGRES_PASSWORD}@{setting.POSTGRES_HOST}:{setting.POSTGRES_PORT}/{setting.POSTGRES_DATABASE}')
async_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def db_conn():
    async with async_maker() as con:
        yield con
