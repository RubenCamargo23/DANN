from pydantic import BaseModel


class OfferCreateRequest(BaseModel):
    postId: str
    userId: str
    description: str
    size: str
    fragile: bool
    offer: float
