from datetime import timedelta, timezone

from models.User import User
from dto.response.UserResponse import UserResponse
from dto.response.LoginResponse import LoginResponse
from config.database import get_async_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from typing import List
from sqlalchemy import ScalarResult as Sc
from dto.request import CreateUserRequest, UpdateUserRequest
from pwdlib import PasswordHash
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime as LocalDateTime
import os

SECRETE_KEY = os.getenv("SECRETE_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRES_IN=os.getenv("ACCESS_TOKEN_EXPIRES_IN")

def verifyPassword(hashed_password: str, plain_passowrd: str) -> bool:
    return PasswordHash.verify(hash=hashed_password, password=plain_passowrd)

def generateToken(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = LocalDateTime.now(timezone.utc) + expires_delta
    else:
        expire = LocalDateTime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode,algorithm=ALGORITHM,SECRETE_KEY=SECRETE_KEY)
    return encode_jwt


async def get_all_users(session:AsyncSession = Depends(get_async_session)) -> list[UserResponse]:
    result: Sc = await session.scalars(select(User))
    users: List[User] = result.all()

    return [UserResponse.model_validate(user) for user in users]

def generatePassowrdhash(password: str) -> str:
    PasswordHash.hash(password)

async def create_user(request : CreateUserRequest,session: AsyncSession = Depends(get_async_session)) -> UserResponse:
    user: User = User(**request.CreateUserRequest.model_dump())
    user.full_name = user.first_name + " " + user.last_name
    password_hash = generatePassowrdhash(user.password)
    user.password = password_hash
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return UserResponse.model_validate(user)


async def update_user(request: UpdateUserRequest, session: AsyncSession = Depends(get_async_session)) -> UserResponse:
    result: Sc = await session.scalar(select(User).where(User.user_id == request.UpdateUserRequest.user_id))
    user: User = result.first()

    if request.UpdateUserRequest.first_name:
        user.first_name = request.UpdateUserRequest.first_name

    if request.UpdateUserRequest.last_name:
        user.last_name = request.UpdateUserRequest.last_name

    if request.UpdateUserRequest.is_active:
        user.is_active = request.UpdateUserRequest.is_active

    if request.UpdateUserRequest.is_superadmin:
        user.is_superuser = request.UpdateUserRequest.is_superadmin

    if request.UpdateUserRequest.username:
        user.username = request.UpdateUserRequest.username

    if request.UpdateUserRequest.password:
        user.password = generatePassowrdhash(request.UpdateUserRequest.password)

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return UserResponse.validate(user)


async def getUserById(user_id: int, session: AsyncSession = Depends(get_async_session)) -> UserResponse:
    result:  Sc = session.scalar(select(User).where(user_id == User.user_id))
    user: User = result.first()

    return UserResponse.validate(user)


async def deleteuserById(user_id: int , session: AsyncSession = Depends(get_async_session)) -> None:
    result: Sc = session.scalar(select(User).where(user_id == User.user_id))
    user: User = result.first()
    session.delete(user)

    await session.commit()

async def login(username: str, password: str, session: AsyncSession = Depends(get_async_session)) -> LoginResponse:
    result: Sc = session.execute(select(User).where(User.username == username))
    user:  User = result.first()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN)
    data = {
        "username": user.username,
        "user_id": user.user_id,
        "name": user.first_name
    }
    token: str = generateToken(data=data, expires_delta=access_token_expires)

    return LoginResponse(token=token, user_id=user.user_id, expiry_in=ACCESS_TOKEN_EXPIRES_IN);