from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.authentication import require_authentication
from app.controllers import users_controller
from app.db.database import get_db
from app.schemas.user_schema import CreateUser, UpdateUser, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/create", response_model=User, status_code=HTTPStatus.CREATED)
def create_user(new_user: CreateUser, session: Session = Depends(get_db)):
    try:
        return users_controller.create_user(session=session, create_user=new_user)
    except Exception as e:
        raise e


@router.get("/", response_model=List[User], status_code=HTTPStatus.FOUND)
@require_authentication
def get_all_users(request: Request, session: Session = Depends(get_db)):
    try:
        users = users_controller.get_users(session=session)
        return users
    except Exception as e:
        raise e


@router.get("/{user_id}", response_model=User, status_code=HTTPStatus.FOUND)
@require_authentication
def get_user(request: Request, user_id: int, session: Session = Depends(get_db)):
    try:
        return users_controller.get_user_by_id(session, user_id=user_id)
    except Exception as e:
        raise e


@router.patch("/{user_id}", status_code=HTTPStatus.ACCEPTED)
@require_authentication
def update_user(
    request: Request, user_id: int, data: UpdateUser, session: Session = Depends(get_db)
):
    try:
        users_controller.update_user(session=session, user_id=user_id, data=data)
        return {f"User id {user_id } successfully updated."}
    except Exception as e:
        raise e


@router.delete("/{user_id}", status_code=HTTPStatus.OK)
@require_authentication
def delete_user(request: Request, user_id: int, session: Session = Depends(get_db)):
    try:
        users_controller.delete_user(session=session, user_id=user_id)
        return {f"User id {user_id } successfully deleted."}
    except Exception as e:
        raise e


@router.post("/{user_id}/product/{product_id}", status_code=HTTPStatus.OK)
@require_authentication
def add_item_to_wishlist(
    request: Request, user_id: int, product_id: int, session: Session = Depends(get_db)
):
    try:
        users_controller.add_item_to_user_wishlist(
            session=session, product_id=product_id, user_id=user_id
        )
        return {f"Product id {product_id } add to user {user_id} wishlist."}
    except Exception as e:
        raise e


@router.delete("/{user_id}/product/{product_id}", status_code=HTTPStatus.OK)
@require_authentication
def delete_item_from_wishlist(
    request: Request, user_id: int, product_id: int, session: Session = Depends(get_db)
):
    try:
        users_controller.delete_item_from_user_wishlist(
            session=session, product_id=product_id, user_id=user_id
        )
        return {f"Product id {product_id } add to user {user_id} wishlist."}
    except Exception as e:
        raise e
