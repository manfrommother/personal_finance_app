from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException
from .security import get_password_hash, verify_password

def get_user(db: Session, user_id : int):
    return db.query(models.User).filter(models.User.id == user_id)

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db : Session, email : str):
    return db.query(models.User).filter(models.User.email == email)

def get_user(db: Session, skip : int=0, limit: int=100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db : Session, user : schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_transactions(db : Session, user_id : int, skip: int, limit: int=100):
    return db.query(models.Transaction).filter(models.Transaction.user_id == user_id).offset(skip).limit(limit).all()

def create_user_transaction(db : Session, transaction: schemas.TransacrionCreate, user_id: int):
    db_transaction = models.Transaction(**transaction.dict(), user_id=user_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def categories(db: Session, skip: int=0, limit: int=100):
    return db.query(models.Category).offset(skip).limit(limit).all()

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username):
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user