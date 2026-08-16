from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreateRequest(BaseModel):
    username: str
    password: str
    email: EmailStr
    dni: Optional[str] = None
    fullName: Optional[str] = None
    phoneNumber: Optional[str] = None


class UserUpdateRequest(BaseModel):
    status: Optional[str] = None
    dni: Optional[str] = None
    fullName: Optional[str] = None
    phoneNumber: Optional[str] = None


class UserAuthRequest(BaseModel):
    username: str
    password: str
