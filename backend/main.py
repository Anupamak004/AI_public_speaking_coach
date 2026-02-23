# backend/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from backend.database import SessionLocal, engine
from backend import models, schemas, auth

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ CORS FIX (THIS IS THE KEY PART)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- REGISTER ----------------
@app.post("/register")
def register(user: schemas.RegisterSchema, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        full_name=user.fullName,
        email=user.email,
        password=auth.hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Registration successful"}

# ---------------- LOGIN ----------------
@app.post("/login")
def login(user: schemas.LoginSchema, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user or not auth.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "message": "Login successful",
        "user_id": db_user.id
    }

# Health check
@app.get("/")
def root():
    return {"status": "Backend running"}