from http import HTTPStatus
from fastapi import FastAPI
from app.db.database import engine
from app.models.user import Base
from app.routers import users_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router.router)
