from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend import models, schemas, auth
from backend.dependencies.auth_dep import get_db

router = APIRouter(prefix="/user", tags=["User"])


# ---------------- GET PROFILE ----------------
@router.get("/profile", response_model=schemas.ProfileResponse)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "fullName": user.full_name,
        "email": user.email
    }


# ---------------- UPDATE PROFILE ----------------
@router.put("/profile")
def update_profile(
    user_id: int,
    data: schemas.ProfileUpdateSchema,
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.full_name = data.fullName
    user.email = data.email

    db.commit()
    return {"message": "Profile updated successfully"}


# ---------------- CHANGE PASSWORD ----------------
@router.put("/change-password")
def change_password(
    user_id: int,
    data: schemas.ChangePasswordSchema,
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not auth.verify_password(data.currentPassword, user.password):
        raise HTTPException(status_code=400, detail="Current password incorrect")

    user.password = auth.hash_password(data.newPassword)
    db.commit()

    return {"message": "Password updated successfully"}