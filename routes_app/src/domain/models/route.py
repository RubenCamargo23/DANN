from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Route(BaseModel):
    """Route domain model."""

    id: Optional[str] = None
    flight_id: str = Field(min_length=1)
    source_airport_code: str = Field(min_length=1)
    source_country: str = Field(min_length=1)
    destiny_airport_code: str = Field(min_length=1)
    destiny_country: str = Field(min_length=1)
    bag_cost: int = Field(ge=0)
    planned_start_date: datetime
    planned_end_date: datetime
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
