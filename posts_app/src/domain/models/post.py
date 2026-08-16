from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Post(BaseModel):
    """Post domain model."""

    id: Optional[str] = None
    route_id: str = Field(min_length=1)
    user_id: str = Field(min_length=1)
    expire_at: datetime
    created_at: Optional[datetime] = None
