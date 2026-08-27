from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
