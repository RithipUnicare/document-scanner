from pydantic import BaseModel
from typing import Optional


class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    username: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False