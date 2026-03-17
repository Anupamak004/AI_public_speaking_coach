# backend/models.py
from sqlalchemy import Column, Integer, String, TIMESTAMP
from backend.database import Base
from sqlalchemy import Float, Text, ForeignKey
from sqlalchemy.orm import relationship
import json
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    
    


from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from datetime import datetime

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    title = Column(String)
    video_path = Column(String)

    score = Column(Float)
    duration = Column(String)

    metrics = Column(Text)
    feedback = Column(Text)
    suggestions = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)  # ✅ ADD THIS