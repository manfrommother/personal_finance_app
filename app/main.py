from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI(title='Personal Finance App')


SQLALCHEMY_DATABASE_URL = 'sqlite:///./finance_app.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread':False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Welcome to Personal Finance App"}

# Здесь будут импортироваться и подключаться роуты из других модулей
# from .api import users, transactions, categories, budgets
# app.include_router(users.router)
# app.include_router(transactions.router)
# app.include_router(categories.router)
# app.include_router(budgets.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
