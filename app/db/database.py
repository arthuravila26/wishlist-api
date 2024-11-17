from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from app.models.user import Base

DATABASE_URI = os.getenv('DB_URI')

engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

try:
    connection = engine.connect()
    print("Database connected!")
    connection.close()
except Exception as e:
    print(f"Database connection failed: {e}")
