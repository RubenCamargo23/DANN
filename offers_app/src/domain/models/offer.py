from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class PackageSize(str, Enum):
    """Enum for package sizes."""

    LARGE = "LARGE"
    MEDIUM = "MEDIUM"
    SMALL = "SMALL"


class Offer(BaseModel):
    """Offer domain model."""

    id: Optional[str] = None
    post_id: str = Field(min_length=1)
    user_id: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=140)
    size: PackageSize
    fragile: bool
    offer: float = Field(ge=0)
    created_at: Optional[datetime] = None
