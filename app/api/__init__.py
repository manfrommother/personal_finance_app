from fastapi import APIRouter
from app.api.endpoints import auth, income, expense

api_router = APIRouter()
api_router.include_router(auth.router, prefix='/auth', tags=['auth'])
api_router.include_router(income.router, prefix='/incomes', tags=['incomes'])
api_router.include_router(expense.router, prefix='/expenses', tags=['expenses'])
