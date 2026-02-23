# backend/schemas.py
from pydantic import BaseModel, EmailStr

class RegisterSchema(BaseModel):
    fullName: str
    email: EmailStr
    password: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str