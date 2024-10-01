from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username : str
    email : str

class UserCreate(BaseModel):
    password : str

class User(BaseModel):
    id : int

    class Config:
        orm_mode = True

class CategoryBase(BaseModel):
    name : str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id : int

    class Config:
        orm_mode = True

class TransactionBase(BaseModel):
    amount : float
    description : Optional[str] = None
    date : Optional[datetime] = None

class TransactionCreate(TransactionBase):
    category_id : int

class TransacrionCreate(TransactionBase):
    category_id : int

class Transaction(TransactionBase):
    id : int
    user_id : int
    category_id : int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None