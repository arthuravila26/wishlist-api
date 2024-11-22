from passlib.context import CryptContext
from sqlalchemy import JSON, Column, Integer, String
from sqlalchemy.ext.mutable import MutableList

from app.db.database import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    wishlist = Column(MutableList.as_mutable(JSON), default=[])

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
