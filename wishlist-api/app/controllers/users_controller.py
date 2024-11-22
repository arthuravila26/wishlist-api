import requests
from sqlalchemy.orm import Session

from app.auth.password import hash_password
from app.models.user import User
from app.utils.exceptions import (
    EmailAlreadyExists,
    ItemDuplicatedInWishList,
    ProductNotFound,
    UserNotFound,
)
from app.utils.logger import logger
import os


def create_user(session: Session, create_user):
    check_email = get_user_by_email(session, create_user.email)

    if check_email:
        logger.error(f"Email {create_user.email} already registered.")
        raise EmailAlreadyExists()

    hash_pass = hash_password(create_user.password)
    user = User(name=create_user.name, email=create_user.email, password=hash_pass)
    session.add(user)
    session.commit()
    session.refresh(user)
    logger.info(f"User {create_user.name} has been created.")
    return user


def get_users(session: Session):
    return session.query(User).all()


def get_user_by_id(session: Session, user_id: int):
    user = session.query(User).filter(User.id == user_id).first()
    if user is None:
        raise UserNotFound()
    return user


def get_user_by_email(session: Session, email: str):
    return session.query(User).filter(User.email == email).first()


def update_user(session: Session, user_id: int, data):
    check_email = get_user_by_email(session, data.email)

    if check_email and check_email.id != user_id:
        logger.error(f"Email {data.email} already registered.")
        raise EmailAlreadyExists()

    user = get_user_by_id(session, user_id)
    user.name = data.name
    user.email = data.email
    user.password = hash_password(data.password)
    session.commit()
    session.refresh(user)
    logger.info(f"User {data.name} Updated.")
    return user


def delete_user(session: Session, user_id: int):
    try:
        user = get_user_by_id(session, user_id)
        session.delete(user)
        session.commit()
        logger.info(f"User {user.name} Deleted.")
        return {"message": "User deleted successfully"}
    except:
        logger.error(f"User id {user_id} Not found.")
        raise UserNotFound()


def add_item_to_user_wishlist(session: Session, user_id: int, product_id: int):
    user = get_user_by_id(session, user_id)
    existing_item = next((item for item in user.wishlist if item.get('ID') == product_id), None)

    if existing_item:
        raise ItemDuplicatedInWishList()

    product_data = send_request_to_get_product(product_id)

    user.wishlist.append(product_data)
    session.commit()


def delete_item_from_user_wishlist(session: Session, user_id: int, product_id: int):
    user = get_user_by_id(session, user_id)

    if next(item for item in user.wishlist if item.get("id") == product_id) is None:
        raise ProductNotFound()

    product_data = send_request_to_get_product(product_id)

    user.wishlist.remove(product_data)
    session.commit()


def send_request_to_get_product(product_id):
    response = requests.get(f"http://{os.getenv("PRODUCT_API")}:8080/product/{product_id}")
    if response.status_code != 200:
        raise ProductNotFound()
    return response.json()
