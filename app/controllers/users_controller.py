from http import HTTPStatus

from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.exceptions import UserNotFound, EmailAlreadyExists, ItemDuplicatedInWishList, ProductNotFound
from app.utils.logger import logger
import requests

def create_user(session: Session, request):
    check_email = get_user_by_email(session, request.email)
    if check_email:
        logger.error(f'Email {request.email} already registered.')
        raise EmailAlreadyExists()
    user = User(name=request.name, email=request.email)
    session.add(user)
    session.commit()
    session.refresh(user)
    logger.info(f'User {request.name} has been created.')
    return user

def get_users(session: Session):
    return session.query(User).all()

def get_user_by_id(session: Session, user_id: int):
    try:
        user = session.query(User).filter(User.id == user_id).first()
        return user
    except:
        logger.error(f'User {user_id} Not found.')
        raise UserNotFound()

def get_user_by_email(session: Session, email: str):
    return session.query(User).filter(User.email == email).first()

def update_user(session: Session, user_id: int, request):
    check_email = get_user_by_email(session, request.email)
    if check_email:
        logger.error(f'Email {request.email} already registered.')
        raise EmailAlreadyExists()
    try:
        user = get_user_by_id(session, user_id)
        user.name = request.name
        user.email = request.email
        session.commit()
        session.refresh(user)
        logger.error(f'User {request.name} Updated.')
        return user
    except:
        logger.error(f'User {request.name} Not found.')
        raise UserNotFound()

def delete_user(session: Session, user_id: int):
    try:
        user = get_user_by_id(session, user_id)
        session.delete(user)
        session.commit()
        logger.info(f'User {user.name} Deleted.')
        return {"message": "User deleted successfully"}
    except:
        logger.error(f'User id {user_id} Not found.')
        raise UserNotFound()

def add_item_to_user_wishlist(session: Session, user_id: int, product_id: int):
    user = get_user_by_id(session, user_id)

    if any(item.get("id") == product_id for item in user.wishlist):
        raise ItemDuplicatedInWishList()

    product_data = send_request_to_get_product(product_id)

    user.wishlist.append(product_data)
    session.commit()

def send_request_to_get_product(product_id):
    response = requests.get(f"http://localhost:8000/api/products/{product_id}")
    if response.status_code != 200:
        raise ProductNotFound()
    return response.json()
