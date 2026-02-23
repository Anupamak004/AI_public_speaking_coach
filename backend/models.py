# backend/models.py
from sqlalchemy import Column, Integer, String, TIMESTAMP
from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)