from sqlalchemy import String, Column, Integer, Float
from app.db.database import Base

class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    brand = Column(String, nullable=False)
    image = Column(String, nullable=False)
    reviewScore = Column(Float, nullable=False)
