# backend/schemas.py
from pydantic import BaseModel, EmailStr

class RegisterSchema(BaseModel):
    fullName: str
    email: EmailStr
    password: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str


# 👇 NEW
class ProfileResponse(BaseModel):
    fullName: str
    email: EmailStr


class ProfileUpdateSchema(BaseModel):
    fullName: str
    email: EmailStr


class ChangePasswordSchema(BaseModel):
    currentPassword: str
    newPassword: str    