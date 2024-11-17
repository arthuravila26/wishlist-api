from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app.models.user import Base
from app.controllers import users_controller
from app import schema

Base.metadata.create_all(bind=engine)

router = APIRouter(prefix='/api/users', tags=['users'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", status_code=HTTPStatus.CREATED)
def create_user(request: schema.User, db: Session = Depends(get_db)):
    return users_controller.create_user(db=db, request=request)

@router.get("/", status_code=HTTPStatus.FOUND)
def get_all_users(db: Session = Depends(get_db)):
    users = users_controller.get_users(db=db)
    return users

@router.get("/{user_id}", status_code=HTTPStatus.FOUND)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = users_controller.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return db_user

@router.patch("/{user_id}", status_code=HTTPStatus.ACCEPTED)
def update_user(user_id: int, request: schema.User, db: Session = Depends(get_db)):
    return users_controller.update_user(db=db, user_id=user_id, request=request)

@router.delete("/{user_id}", status_code=HTTPStatus.OK)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return users_controller.delete_user(db, user_id=user_id)
