from config.database import get_async_session, Base
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from typing import Optional



class UserDocuments(Base):
    __tablename__ = "user_documents"

    user_document_id: Integer = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id: Integer = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    document_id: Integer = Column(Integer, nullable=False)
    document_name:Optional[String] = Column(String, nullable=True)

    users: relationship = relationship("User", back_populates="user_documents")