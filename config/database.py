from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, engine as Engine
from collections.abc import AsyncGenerator
from sqlalchemy.engine import URL
import os

class Base(DeclarativeBase):
    pass

POSTGRES_URL = os.getenv("POSTGRES_URL")
DATABASE_USERNAME = os.getenv("POSTGRES_USERNAME")
DATABASE_PASSWORD = os.getenv("POSTGRES_PASSWORD")

DATABASE_URL = URL.create(
    drivername="postgresql+asyncpg",
    username=DATABASE_USERNAME,
    password=DATABASE_PASSWORD,
    host=POSTGRES_URL,
    database="document_scanner",
)

#DATABASE_URL = f"postgresql+asyncpg://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{POSTGRES_URL}"

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

async def async_db_create() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_session() -> AsyncGenerator:
    async with async_session_maker() as session:
        yield session
