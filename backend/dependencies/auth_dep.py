# backend/dependencies/auth_dep.py
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend import models

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user