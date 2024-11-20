from fastapi import FastAPI

import app.models
from app.db.database import Base, engine
from app.routers import auth_router, products_router, users_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router.router)
app.include_router(products_router.router)
app.include_router(auth_router.router)
