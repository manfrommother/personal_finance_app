from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ExpenseBase(BaseModel):
    amount: float
    description: Optional[str]=None
    category_id: int
    date: datetime

class ExpenseCreate(ExpenseBase):
    pass 

class ExpenseUpdate(ExpenseBase):
    amount: Optional[float]=None
    category_id: Optional[int]=None
    date: Optional[datetime]=None

class Expense(ExpenseBase):
    id: int
    user_id: int
    category_at: datetime
    update_at: datetime

    class Config:
        orm_mode = True