from sqlalchemy.orm import Session
from app.models import Income
from app.schemas.income import IncomeCreate, IncomeUpdate

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