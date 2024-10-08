from pydantic import BaseModel
from datetime import datetime
from typing import List

class FinancialSummary(BaseModel):
    total_income: float
    total_expense: float
    balance: float
    start_date: datetime
    end_date: datetime

class CategorySummary(BaseModel):
    category_id: int
    total_amount: float

class DetailedFinancialReport(FinancialSummary):
    income_by_category: List[CategorySummary]
    expense_by_category: List[CategorySummary]

