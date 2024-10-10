from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud import financial_goal as financial_goal_crud
from app.schemas.finance_goal import FinancialGoal, FinancialGoalCreate, FinancialGoalUpdate
from app.core.security import get_current_user
from app.db.session import get_db
from app.models import User

router = APIRouter()

@router.post('/', response_model=FinancialGoal)
def create_financial_goal(
    goal: FinancialGoalCreate,
    db: Session=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    return financial_goal_crud.create_financial_goal(db=db, goal=goal, user_id=current_user.id)

@router.get('/', response_model=List[FinancialGoal])
def read_financial_goals(
    skip: int=0,
    limit: int=0,
    db: Session=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    goals = financial_goal_crud.get_finance_goal(db, user_id=current_user.id, skip=skip, limit=limit)
    return goals

#TODO дописать функции с удалением и обновлением финансовых целей