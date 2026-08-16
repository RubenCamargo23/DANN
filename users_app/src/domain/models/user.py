from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserStatus(str, Enum):
    """Enum for user status."""

    POR_VERIFICAR = "POR_VERIFICAR"
    NO_VERIFICADO = "NO_VERIFICADO"
    VERIFICADO = "VERIFICADO"


class User(BaseModel):
    """User domain model."""

    id: Optional[str] = None
    username: str = Field(min_length=1)
    email: EmailStr
    phone_number: Optional[str] = None
    dni: Optional[str] = None
    full_name: Optional[str] = None
    password: str = Field(min_length=1)
    salt: Optional[str] = None
    token: Optional[str] = None
    status: UserStatus = UserStatus.POR_VERIFICAR
    expire_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
