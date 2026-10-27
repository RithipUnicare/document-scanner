from pydantic import BaseModel
from typing import Optional

class UpdateUserRequest(BaseModel):
    user_id: int
    first_name:Optional[str]
    last_name: Optional[str]
    is_active: Optional[bool]
    is_superadmin: Optional[bool]
    username: Optional[str]
    password: Optional[str]