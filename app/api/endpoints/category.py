from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud import category as category_crud
from app.schemas.category import Category, CategoryCreate, CategoryUpdate
from app.core.security import get_current_user
from app.db.session import get_db
from app.models import User

router = APIRouter()

@router.post('/', response_model=Category)
def create_category(
    category: CategoryCreate,
    db: Session=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    return category_crud.create_category(db=db, category=category, user_id=current_user.id)

@router.get('/', response_model=List[Category])
def read_categories(
    skip: int=0,
    limit: int=100,
    db: Session=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    categories = category_crud.get_category(db, user_id=current_user.id, skip=skip, limit=limit)
    return categories

@router.get('/{category_id}', response_model=Category)
def read_category(
    category_id: int,
    db: Session=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    category = category_crud.get_category(db, category_id=category_id, user_id=current_user.id)
    if category is None:
        raise HTTPException(status_code=404, detail='Категория не найдена')
    return category

@router.put('/{category_id}', response_model=Category)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    updated_category = category_crud.update_category(db, category_id=category_id, category=category, user_id=current_user.id)
    if update_category is None:
        raise HTTPException(status_code=404, detail='Категория не найдена')
    return updated_category

@router.delete('/{category_id}', response_model=Category)
def delete_category(
    category_id: int,
    db: Session=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    delete_category = category_crud.delete_category(db, category_id=category_id, user_id=current_user.id)
    if delete_category is None:
        raise HTTPException(status_code=404, detail='Категория не найдена')
    return delete_category