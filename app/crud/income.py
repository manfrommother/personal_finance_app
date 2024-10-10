from sqlalchemy.orm import Session
from app.models import Income, Expense
from app.schemas.income import IncomeCreate, IncomeUpdate
from datetime import datetime

def create_income(db: Session, income: IncomeCreate, user_id: int):
    db_income = Income(**income.dict(), user_id=user_id)
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income

def get_incomes(db: Session, income_id: int, user_id: int):
    return db.query(Income).filter(Income.id == income_id, Income.user_id).first()

def update_income(db: Session, income_id: int, income: IncomeCreate, user_id: int):
    db_income = get_incomes(db, income_id, user_id)
    if db_income:
        update_data = income.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_income, key, value)
        db.add(db_income)
        db.commit()
        db.refresh(db_income)
    return db_income

def delete_income(db: Session, income_id: str, user_id: int):
    db_income = get_incomes(db, income_id, user_id)
    if db_income:
        db.delete(db_income)
        db.commit()
    return db_income

def get_filtered_items(db: Session, user_id: int, skip: int=0, limit: int=100,
                       start_date: datetime=None, end_date: datetime=None,
                       caregory_id: int=None, min_amount: float=None, max_amount: float=None):
    query = db.query(Income if 'income' in __name__ else Expense).filter(
        (Income if 'income' in __name__ else Expense).user_id == user_id)
    
    if start_date:
        query = query.filter((Income if 'income' in __name__ else Expense).date >= start_date)
    if end_date:
        query = query.filter((Income if 'income' in __name__ else Expense).date <= end_date)
    if caregory_id:
        query = query.filter((Income if 'income' in __name__ else Expense).category_id == caregory_id)
    if min_amount:
        query = query.filter((Income if 'income' in __name__ else Expense).amount >= min_amount)
    if max_amount:
        query = query.filter((Income if 'income' in __name__ else Expense).amount <= max_amount)

    return query.offset(skip).limit(limit).all()

def get_filtered_items_count(db: Session, user_id: int, 
                             start_date: datetime = None, end_date: datetime = None, 
                             category_id: int = None, min_amount: float = None, max_amount: float = None):
    query = db.query(Income if "income" in __name__ else Expense).filter(
        (Income if "income" in __name__ else Expense).user_id == user_id
    )
    
    if start_date:
        query = query.filter((Income if "income" in __name__ else Expense).date >= start_date)
    if end_date:
        query = query.filter((Income if "income" in __name__ else Expense).date <= end_date)
    if category_id:
        query = query.filter((Income if "income" in __name__ else Expense).category_id == category_id)
    if min_amount:
        query = query.filter((Income if "income" in __name__ else Expense).amount >= min_amount)
    if max_amount:
        query = query.filter((Income if "income" in __name__ else Expense).amount <= max_amount)
    
    return query.count()