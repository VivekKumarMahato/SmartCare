from pydantic import BaseModel, EmailStr
from app.models.enums import UserRole

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole = UserRole.patient


class UserLogin(BaseModel):
    email: EmailStr
    password: str
