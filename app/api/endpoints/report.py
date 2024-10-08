from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.crud import report as report_crud
from app.schemas.report import FinancialSummary, DetailedFinancialReport
from app.core.security import get_current_user
from app.db.session import get_db
from app.models import User

router = APIRouter()

@router.get('/summary', response_model=FinancialSummary)
def get_financial_summary(
    start_date: datetime=None,
    end_date: datetime=None,
    db: Session=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    if not start_date:
        start_date = datetime.now() - timedelta(days=30)
    if not end_date:
        end_date = datetime.now()

    total_income = report_crud.get_total_income(db, current_user.id, start_date, end_date)
    total_expense = report_crud.get_total_expense(db, current_user.id, start_date, end_date)
    balance = report_crud.get_balance(db, current_user.id)

    return FinancialSummary(
        total_income=total_income,
        total_expense=total_expense,
        balance=balance,
        start_date=start_date,
        end_date=end_date
    )

@router.get('/detailed', response_model=DetailedFinancialReport)
def get_detailed_financial_report(
    start_date: datetime = None,
    end_date: datetime=None,
    db: Session=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    if not start_date:
        start_date = datetime.now() - timedelta(days=30)
    if not end_date:
        end_date = datetime.now()

    summary = get_financial_summary(start_date, end_date, db, current_user)
    income_by_category = report_crud.get_category_summary(db, current_user.id, start_date, end_date, 'income')
    expense_by_category = report_crud.get_category_summary(db, current_user.id, start_date, end_date, 'expense')

    return DetailedFinancialReport(
        **summary.dict(),
        income_by_category=income_by_category,
        expense_by_category=expense_by_category
    )