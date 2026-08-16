from datetime import datetime

from pydantic import BaseModel


class PostCreateRequest(BaseModel):
    routeId: str
    expireAt: datetime
    userId: str
