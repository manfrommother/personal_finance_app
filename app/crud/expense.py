from sqlalchemy.orm import Session
from app.models import Expense, Income
from app.schemas.expense import ExpenseCreate, ExpenseUpdate
from datetime import datetime

def create_expense(db: Session, expense: ExpenseCreate, user_id: int):
    db_expense = Expense(**expense.dict(), user_id=user_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

def get_expenses(db: Session, user_id: int, skip: int=0, limit: int=100):
    return db.query(Expense).filter(Expense.user_id == user_id).offset(skip).limit(limit).all()

def get_expense(db: Session, expense_id: int, user_id: int):
    return db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == user_id).first()

def update_expense(db: Session, expense_id: int, expense: ExpenseUpdate, user_id: int):
    db_expense = get_expense(db, expense_id, user_id)
    if db_expense:
        update_data = expense.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_expense, key, value)
        db.add(db_expense)
        db.commit()
        db.refresh(db_expense)
    return db_expense

def delete_expense(db: Session, expense_id: int, user_id: int):
    db_expense = get_expense(db, expense_id, user_id)
    if db_expense:
        db.delete(db_expense)
        db.commit()
    return db_expense

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