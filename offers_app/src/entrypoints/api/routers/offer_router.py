from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import ValidationError

from assembly import (
    build_count_offers_use_case,
    build_create_offer_use_case,
    build_delete_offer_use_case,
    build_get_offer_use_case,
    build_list_offers_use_case,
    build_reset_offers_use_case,
)
from domain.models.offer import Offer
from domain.use_cases.base_use_case import BaseUseCase
from entrypoints.api.schemas import OfferCreateRequest
from errors import OfferNotFoundError

router = APIRouter(prefix="/offers")


def _serialize(offer: Offer) -> dict:
    return {
        "id": offer.id,
        "postId": offer.post_id,
        "description": offer.description,
        "size": offer.size,
        "fragile": offer.fragile,
        "offer": offer.offer,
        "createdAt": offer.created_at.isoformat(),
        "userId": offer.user_id,
    }


@router.get("/ping", response_class=PlainTextResponse)
def health_check():
    """Healthcheck endpoint."""
    return "pong"


@router.get("/count")
def count_offers(use_case: BaseUseCase = Depends(build_count_offers_use_case)):
    """Count stored offers."""
    return {"count": use_case.execute()}


@router.post("/reset")
def reset_offers(use_case: BaseUseCase = Depends(build_reset_offers_use_case)):
    """Delete all offers."""
    use_case.execute()
    return {"msg": "Todos los datos fueron eliminados"}


@router.post("", status_code=201)
def create_offer(
    payload: OfferCreateRequest,
    use_case: BaseUseCase = Depends(build_create_offer_use_case),
):
    """Create a new offer."""
    try:
        offer = Offer(
            post_id=payload.postId,
            user_id=payload.userId,
            description=payload.description,
            size=payload.size,
            fragile=payload.fragile,
            offer=payload.offer,
        )
    except ValidationError as err:
        raise HTTPException(status_code=412, detail=str(err))

    created = use_case.execute(offer)
    return {
        "id": created.id,
        "userId": created.user_id,
        "createdAt": created.created_at.isoformat(),
    }


@router.get("")
def list_offers(
    post: Optional[str] = None,
    owner: Optional[str] = None,
    use_case: BaseUseCase = Depends(build_list_offers_use_case),
):
    """List/filter offers."""
    offers = use_case.execute(post_id=post, owner_id=owner)
    return [_serialize(o) for o in offers]


@router.get("/{offer_id}")
def get_offer(
    offer_id: str, use_case: BaseUseCase = Depends(build_get_offer_use_case)
):
    """Get an offer by id."""
    try:
        offer = use_case.execute(offer_id)
    except OfferNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))
    return _serialize(offer)


@router.delete("/{offer_id}")
def delete_offer(
    offer_id: str, use_case: BaseUseCase = Depends(build_delete_offer_use_case)
):
    """Delete an offer by id."""
    try:
        use_case.execute(offer_id)
    except OfferNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))
    return {"msg": "la oferta fue eliminada"}
