from fastapi import FastAPI, UploadFile, File
import shutil
import os
from fastapi.middleware.cors import CORSMiddleware
from inference.run_inference import run_inference
from db_connection.database import engine, SessionLocal
from db_connection import db_model
from db_connection import schemas
from db_connection.auth import create_access_token, hash_password, verify_password


db_model.Base.metadata.create_all(bind=engine)

app = FastAPI()

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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


UPLOAD_DIR = "uploaded_videos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/analyze")
async def analyze_video(file: UploadFile = File(...)):
    video_path = f"temp/{file.filename}"
    os.makedirs("temp", exist_ok=True)

    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    scores = run_inference(video_path)  # must return dict

    return {
        "status": "success",
        "scores": scores
    }


@app.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(db_model.User).filter(db_model.User.username == user.username).first()

    if not db_user:
        hashed_password = hash_password(user.password)
        new_user = db_model.User(
            username=user.username,
            password=hashed_password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        db_user = new_user 

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": db_user.username})

    return {"access_token": access_token, "token_type": "bearer"}

