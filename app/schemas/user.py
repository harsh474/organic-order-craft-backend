from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    phone: str
    address: Optional[str] = None

class UserRead(BaseModel):
    id: int
    email: EmailStr
    phone: str
    address: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    phone: Optional[str] = None
    address: Optional[str] = None
