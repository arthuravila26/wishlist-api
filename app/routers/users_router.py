from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.controllers import users_controller
from app.schemas.user_schema import User


router = APIRouter(prefix='/api/users', tags=['users'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", status_code=HTTPStatus.CREATED)
def create_user(request: User, session: Session = Depends(get_db)):
    return users_controller.create_user(session=session, request=request)

@router.get("/", status_code=HTTPStatus.FOUND)
def get_all_users(session: Session = Depends(get_db)):
    users = users_controller.get_users(session=session)
    return users

@router.get("/{user_id}", status_code=HTTPStatus.FOUND)
def get_user(user_id: int, session: Session = Depends(get_db)):
    user = users_controller.get_user_by_id(session, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return user

@router.patch("/{user_id}", status_code=HTTPStatus.ACCEPTED)
def update_user(user_id: int, request: User, session: Session = Depends(get_db)):
    return users_controller.update_user(session=session, user_id=user_id, request=request)

@router.delete("/{user_id}", status_code=HTTPStatus.OK)
def delete_user(user_id: int, session: Session = Depends(get_db)):
    return users_controller.delete_user(session=session, user_id=user_id)
