from sqlalchemy import String, Column, Integer, JSON
from sqlalchemy.ext.mutable import MutableList

from app.db.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    wishlist = Column(MutableList.as_mutable(JSON), default=[])
