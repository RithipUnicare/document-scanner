from config.database import get_async_session, Base
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, SQLAlchemyBaseUserTable
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator

class User(SQLAlchemyBaseUserTableUUID, Base):
    pass

async def get_user_db(session: AsyncSession = Depends(get_async_session)) -> AsyncGenerator[User, None]:
    yield SQLAlchemyBaseUserTable(session, User)

