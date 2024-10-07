from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class USer(UserBase):
    id: int
    created_at: datetime
    updated_at = datetime

    class Config:
        orm_model = True

class Token(BaseModel):
    access_token:str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    