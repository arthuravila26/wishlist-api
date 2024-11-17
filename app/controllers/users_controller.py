from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.exceptions import UserNotFound, EmailAlreadyExists
from app.utils.logger import logger

def create_user(db: Session, request):
    check_email = get_user_by_email(db, request.email)
    if check_email:
        logger.error(f'Email {request.email} already registered.')
        raise EmailAlreadyExists()
    db_user = User(name=request.name, email=request.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f'User {request.name} has been created.')
    return db_user

def get_users(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def update_user(db: Session, user_id: int, request):
    check_email = get_user_by_email(db, request.email)
    if check_email:
        logger.error(f'Email {request.email} already registered.')
        raise EmailAlreadyExists()
    try:
        user = get_user_by_id(db, user_id)
        user.name = request.name
        user.email = request.email
        db.commit()
        db.refresh(user)
        logger.error(f'User {request.name} Updated.')
        return user
    except:
        logger.error(f'User {request.name} Not found.')
        raise UserNotFound()

def delete_user(db: Session, user_id: int):
    try:
        user = get_user_by_id(db, user_id)
        db.delete(user)
        db.commit()
        logger.info(f'User {user.name} Deleted.')
        return {"message": "User deleted successfully"}
    except:
        logger.error(f'User {user.name} Not found.')
        raise UserNotFound()
