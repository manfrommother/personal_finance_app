from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.crud import user as user_crud
from app.core.security import create_access_token
from app.core.config import settings
from app.schemas import User, UserCreate, Token
from app.db.session import get_db

router = APIRouter()

@router.post('/register', response_model=User)
def register(user: UserCreate, db: Session=Depends(*get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Адрес электронной почты уже зарегистрирован')
    return user_crud.create_user(db=db, user=user)

@router.post('/token', response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)):
    user = user_crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный логин или пароль',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    access_toke_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.email}, expires_delta=access_toke_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}