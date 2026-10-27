from pydantic import BaseModel

class LoginResponse(BaseModel):
    token: str
    user_id: int
    expiry_in:int
