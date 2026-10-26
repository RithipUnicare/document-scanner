from models.User import User
from dto.response.UserResponse import UserResponse
from config.database import get_async_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from sqlalchemy import ScalarResult as Sc

async def get_all_users(session:AsyncSession = Depends(get_async_session)) -> list[UserResponse]:
    result: Sc = await session.scalars(select(User))
    users: List[User] = result.all()

    return [UserResponse.model_validate(user) for user in users]

async def create_user():
    pass
