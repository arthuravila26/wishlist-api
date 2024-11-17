from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URI = os.getenv('DB_URI')

engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

try:
    connection = engine.connect()
    print("Database connected!")
    connection.close()
except Exception as e:
    print(f"Database connection failed: {e}")
