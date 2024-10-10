from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FinancialGoalBase(BaseModel):
    name: str
    target_amount = float
    deadline: datetime

class FinancialGoalCreate(FinancialGoalBase):
    pass

class FinancialGoalUpdate(BaseModel):
    name: Optional[str] = None
    target_amount: Optional[float] = None
    current_amount: Optional[float] = None
    deadline: Optional[datetime] = None

class FinancialGoal(FinancialGoalBase):
    id: int
    user_id: int
    current_amount: float
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_model = True