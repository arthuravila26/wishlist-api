import os
from datetime import datetime, timedelta, timezone
from functools import wraps
from http import HTTPStatus

import jwt
from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from app.controllers.users_controller import get_user_by_email
from app.models import User

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def authenticate_user(email: str, password: str, session: Session):
    user = get_user_by_email(session, email)
    if not user or not User.verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user


def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return True
    except jwt.PyJWTError:
        raise HTTPException(status_code=403, detail="Invalid token")


def require_authentication(func):
    @wraps(func)
    def wrapper(request: Request, *args, **kwargs):
        authorization: str = request.headers.get("Authorization")
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Token is missing or invalid format",
            )

        token = authorization.split(" ")[1]

        if not decode_jwt_token(token):
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail="Invalid token"
            )
        return func(request, *args, **kwargs)

    return wrapper
