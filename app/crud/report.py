from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Income, Expense
from datetime import datetime, timedelta

def get_total_income(db: Session, user_id: int, start_date: datetime, end_date: datetime):
    return db.query(func.sum(Income.amount)).filter(
        Income.user_id == user_id,
        Income.date >= start_date,
        Income.date <= end_date
    ).scalar() or 0

def get_total_expense(db: Session, user_id: int, start_date: datetime, end_date: datetime):
    return db.query(func.sum(Expense.amount)).filter(
        Expense.user_id == user_id,
        Expense.date >= start_date,
        Expense.date <= end_date
    ).scalar() or 0

def get_balance(db: Session, user_id: int):
    total_income = db.query(func.sum(Income.amount)).filter(Income.user_id == user_id).scalar() or 0
    total_expense = db.query(func.sum(Expense.amount)).filter(Expense.user_id == user_id).scalar() or 0
    return total_income - total_expense

def get_category_summary(db: Session, user_id: int, start_date: datetime, end_date: datetime, transaction_type: str):
    if transaction_type == 'income':
        model = Income
    elif transaction_type == 'expense':
        model = Expense
    else: 
        raise ValueError('Недопустимый тип транзакции')
    
    return db.query(
        model.category_id,
        func.sum(model.amount).label('total_amount')
    ).filter(
        model.user_id == user_id,
        model.date >= start_date,
        model.date <= end_date
    ).group_by(model.category_id).all()

