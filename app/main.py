from fastapi import FastAPI
from app.core.config import settings
from app.api import api_router

app = FastAPI(title='Personal Finance API')

app.include_router(api_router)

@app.get('/')
async def root():
    return {'message': 'Welcome to Personal Finance API'}

