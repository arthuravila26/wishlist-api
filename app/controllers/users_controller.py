from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.exceptions import UserNotFound, EmailAlreadyExists
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
    return session.query(User).filter(User.id == user_id).first()

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
        logger.error(f'User {user.name} Not found.')
        raise UserNotFound()

def add_item_to_user_wishlist(product_id: int, user_id):
    pass

def send_request_to_get_product(product_id):
    response = requests.get(f"http://localhost:8000/api/products/{product_id}")
    return response.json()

