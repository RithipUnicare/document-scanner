from config.database import get_async_session, Base
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, SQLAlchemyBaseUserTable
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship, CascadeOptions
from typing import List

class User(Base):
    __tablename__ = "users"

    user_id: Integer = Column(Integer,primary_key=True, autoincrement=True, index=True)
    first_name: String = Column(String, nullable=False)
    last_name: String = Column(String, nullable=False)
    full_name: String = Column(String, nullable=False)
    email: String = Column(String, nullable=False, unique=True)
    username: String = Column(String, nullable=False, unique=True)
    password: String = Column(String, nullable=False)
    is_active: Boolean = Column(Boolean, nullable=False)
    is_superuser: Boolean = Column(Boolean, nullable=False)
    created_at: DateTime = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: DateTime = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    user_documents: relationship = relationship("UserDocuments", back_populates="users", cascade="all, delete-orphan")

async def get_user_db(session: AsyncSession = Depends(get_async_session)) -> AsyncGenerator[User, None]:
    yield session.query(User).first()

