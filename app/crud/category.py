from sqlalchemy.orm import Session
from app.models import Category
from app.schemas.category import CategoryCreate, CategoryUpdate

def create_category(db: Session, category: CategoryCreate, user_id: int):
    db_category = Category(**category.dict(), user_id=user_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_category(db: Session, category_id: int, user_id: int):
    return db.query(Category).filter(Category.id == category_id, Category.user_id == user_id).first()

def update_category(db: Session, category_id: int, category: CategoryUpdate, user_id:int):
    db_category = get_category(db, category_id, user_id)
    if db_category:
        update_data = category.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_category, key, value)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int, user_id: int):
    db_category = get_category(db, category_id, user_id)
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category