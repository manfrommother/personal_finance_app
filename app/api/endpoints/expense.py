from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud import expense as expense_crud
from app.schemas.expense import Expense, ExpenseCreate, ExpenseUpdate
from app.core.security import get_current_user
from app.db.session import get_db
from app.models import User

router = APIRouter

@router.post('/', response_model=Expense)
def create_expense(
    expense: ExpenseCreate,
    db: Session=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    return expense_crud.create_expense(db, expense=expense, user_id=current_user.id)

@router.get('/', response_model=List[Expense])
def read_expenses(
    skip: int=0,
    limit: int=100,
    db: Session=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    expenses = expense_crud.get_expenses(db, user_id=current_user.id, skip=skip, limit=limit)
    return expenses

@router.get('/{expense_id}', response_model=Expense)
def read_expense(
    expense_id: int,
    db: Session=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    expense = expense_crud.get_expense(db, expense_id=expense_id, user_id=current_user.id)
    if expense is None:
        raise HTTPException(status_code=404, detail='Расход не найден')
    return expense

@router.put('/{expense_id}', response_model=Expense)
def update_expense(
    expense_id: int,
    expense: ExpenseUpdate,
    db: Session=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    delete_expense = expense_crud.delete_expense(db, expense_id=expense_id, user_id=current_user.id)
    if delete_expense is None:
        raise HTTPException(status_code=404, detail='Расход не найден')
    return delete_expense