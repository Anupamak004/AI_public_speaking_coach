# backend/main.py
import cv2
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from backend.database import SessionLocal, engine
from backend import models, schemas, auth
from backend.models import Base

from fastapi import UploadFile, File
import shutil
import os
from fastapi.middleware.cors import CORSMiddleware


from inference.run_inference import run_inference
import json
from backend.routers import user


app = FastAPI()
# Create tables
models.Base.metadata.create_all(bind=engine)
app.include_router(user.router)

from fastapi.staticfiles import StaticFiles

app.mount("/videos", StaticFiles(directory="uploaded_videos"), name="videos")
# ✅ CORS FIX (THIS IS THE KEY PART)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
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


UPLOAD_DIR = "uploaded_videos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

from fastapi import Form

@app.post("/analyze")
async def analyze_video(
    file: UploadFile = File(...),
    user_id: int = Form(...),
    db: Session = Depends(get_db)
):
    video_path = f"uploaded_videos/{file.filename}"

    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # -------- duration --------
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    duration_seconds = frame_count / fps if fps else 0
    cap.release()

    duration_str = f"{int(duration_seconds//60)}:{int(duration_seconds%60):02d} min"

    # -------- STEP 1: Create session --------
    new_session = models.Session(
        user_id=user_id,
        title="Practice Session",
        video_path=video_path,
        score=0,
        duration=duration_str,
        metrics="{}",
        feedback="{}",
        suggestions="[]"
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    session_id = new_session.id

    # ❗ VERY IMPORTANT: CLOSE DB BEFORE LONG TASK
    db.close()

    # -------- STEP 2: Run inference --------
    scores = run_inference(video_path)

    overall_score = sum(scores["scores"].values()) / len(scores["scores"])

    # -------- STEP 3: NEW DB CONNECTION --------
    db = SessionLocal()

    session = db.query(models.Session).filter(models.Session.id == session_id).first()

    if session:
        session.score = overall_score
        session.metrics = json.dumps(scores["scores"])
        session.feedback = json.dumps(scores["feedback"])
        session.suggestions = json.dumps(scores["suggestions"])

        db.commit()

    db.close()

    return {
        "status": "success",
        "scores": scores
    }


@app.get("/sessions/{user_id}")
def get_sessions(user_id: int, db: Session = Depends(get_db)):

    sessions = (
        db.query(models.Session)
        .filter(models.Session.user_id == user_id)
        .order_by(models.Session.id.desc())
        .all()
    )

    results = []

    for s in sessions:
        results.append({
    "id": s.id,
    "title": s.title,
    "score": s.score,
    "duration": s.duration,
    "date": s.created_at.strftime("%d %b %Y"),
    "video_path": s.video_path,   # ⭐ ADD THIS
    "metrics": json.loads(s.metrics),
    "feedback": json.loads(s.feedback),
    "suggestions": json.loads(s.suggestions)
})

    return results