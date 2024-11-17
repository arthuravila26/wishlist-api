from fastapi import FastAPI
from app.db.database import Base, engine
import app.models
from app.routers import users_router, products_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router.router)
app.include_router(products_router.router)
