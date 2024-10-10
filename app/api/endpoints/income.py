from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.crud import income as income_crud, expense as expense_crud
from app.schemas.income import Income, IncomeCreate, IncomeUpdate
from app.core.security import get_current_user
from app.db.session import get_db
from app.models import User
from datetime import datetime
from math import ceil

router = APIRouter()

@router.post('/', response_model=Income)
def create_income(
    income: IncomeCreate,
    db: Session=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    return income_crud.create_income(db=db, income=income, user_id=current_user.id)

@router.get('/', response_model=List[Income])
def read_incomes(
    skip: int=0,
    limit: int=100,
    db: Session=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    incomes = income_crud.get_incomes(db, user_id=current_user.id, skip=skip, limit=limit)
    return incomes

@router.get('/{income_id}', response_model=Income)
def update_income(
    income_id: int,
    income: IncomeUpdate,
    db: Session=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    update_income = income_crud.update_income(db, income_id=income_id, income=income, user_id=current_user.id)
    if update_income is None:
        raise HTTPException(status_code=404, detail='Доход не найден')
    return update_income

@router.delete('/{income_id}', response_model=Income)
def delete_income(
    income_id: int,
    db: Session=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    delete_income = income_crud.delete_income(db, income_id=income_id, user_id=current_user.id)
    if delete_income is None:
        raise HTTPException(status_code=404, detail='Доход не найден')
    return delete_income

@router.get('/', response_model=dict)
def read_items(
    skip: int=Query(0, ge=0),
    limit: int=Query(100, ge=1, le=1000),
    start_date: datetime=None,
    end_date: datetime=None,
    category_id: int=None,
    min_amount: float=None,
    max_amount: float=None,
    db: Session=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    crud_model = income_crud if 'income' in __name__ else expense_crud
    items = crud_model.get_filtered_items(
        db, current_user.id, skip, limit, start_date, end_date, category_id, min_amount, max_amount)
    

    total_count = crud_model.get_filtered_items_count(
        db, current_user.id, start_date, end_date, category_id, min_amount, max_amount
    )

    return{
        'items': items,
        'total_count': total_count,
        'page': skip // limit + 1,
        'total_pages': ceil(total_count / limit)
    }