from http import HTTPStatus

from fastapi import APIRouter, Depends
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
    try:
        users_controller.create_user(session=session, request=request)
    except Exception as e:
        raise e

@router.get("/", status_code=HTTPStatus.FOUND)
def get_all_users(session: Session = Depends(get_db)):
    try:
        users_controller.get_users(session=session)
    except Exception as e:
        raise e

@router.get("/{user_id}", status_code=HTTPStatus.FOUND)
def get_user(user_id: int, session: Session = Depends(get_db)):
    try:
        return users_controller.get_user_by_id(session, user_id=user_id)
    except Exception as e:
        raise e

@router.patch("/{user_id}", status_code=HTTPStatus.ACCEPTED)
def update_user(user_id: int, request: User, session: Session = Depends(get_db)):
    try:
        users_controller.update_user(session=session, user_id=user_id, request=request)
        return {f"User id {user_id } successfully updated."}
    except Exception as e:
        raise e

@router.delete("/{user_id}", status_code=HTTPStatus.OK)
def delete_user(user_id: int, session: Session = Depends(get_db)):
    try:
        users_controller.delete_user(session=session, user_id=user_id)
        return {f"User id {user_id } successfully deleted."}
    except Exception as e:
        raise e

@router.post("/{user_id}/product/{product_id}", status_code=HTTPStatus.OK)
def add_item_to_wishlist(user_id: int, product_id: int, session: Session = Depends(get_db)):
    try:
        users_controller.add_item_to_user_wishlist(session=session, product_id=product_id,user_id=user_id)
        return {f"Product id {product_id } add to user {user_id} wishlist."}
    except Exception as e:
        raise e
