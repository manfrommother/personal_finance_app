from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CategoryBase(BaseModel):
    name: str
    income: str

class CategoryCreate(CategoryBase):
    pass 

class CategoryUpdate(CategoryBase):
    name: Optional[str] = None
    income: Optional[str] = None

class Category(CategoryBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True