from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class IncomeBase(BaseModel):
    amount: float
    description: Optional[str] = None
    category_id: int
    date: datetime

class IncomeCreate(IncomeBase):
    pass 

class IncomeUpdate(IncomeBase):
    amount: Optional[float] = None
    category_id: Optional[int] = None
    date: Optional[datetime] = None

class Income(IncomeBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True