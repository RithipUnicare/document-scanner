from pydantic import BaseModel
from typing import List


class UserResponse(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    full_name: str
    email: str
    username: str
    is_active: bool
    is_superuser: bool
    created_at: str
    updated_at: str

