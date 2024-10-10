from sqlalchemy.orm import Session
from app.models import FinancialGoal
from app.schemas.finance_goal import FinancialGoalCreate, FinancialGoalUpdate

def create_financial_goal(db: Session, goal: FinancialGoalCreate, user_id: int):
    db_goal = FinancialGoal(**goal.dict(), user_id=user_id)
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

def get_finance_goal(db: Session, user_id: int, skip: int=0, limit: int=100):
    return db.query(FinancialGoal).filter(FinancialGoal.user_id == user_id).offset(skip).limit(limit).all()

def update_finance_goal(db: Session, goal_id: int, goal: FinancialGoalUpdate, user_id: int):
    db_goal = get_finance_goal(db, goal_id, user_id)
    if db_goal:
        update_data = goal.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_goal, key, value)
        db.add(db_goal)
        db.commit()
        db.refresh(db_goal)
    return db_goal

def delete_financial_goal(db: Session, goal_id: int, user_id : int):
    db_goal = get_finance_goal(db, goal_id, user_id)
    if db_goal:
        db.delete(db_goal)
        db.commit()
    return db_goal

