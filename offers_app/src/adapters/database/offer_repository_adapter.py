from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from adapters.database.offer_model import OfferModel, generate_uuid
from domain.models.offer import Offer
from domain.ports.offer_repository_port import OfferRepositoryPort


def _model_to_entity(model: OfferModel) -> Offer:
    return Offer(
        id=model.id,
        post_id=model.post_id,
        user_id=model.user_id,
        description=model.description,
        size=model.size,
        fragile=model.fragile,
        offer=model.offer,
        created_at=model.created_at,
    )


class SQLAlchemyOfferRepositoryAdapter(OfferRepositoryPort):
    """PostgreSQL implementation of OfferRepositoryPort using SQLAlchemy."""

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def create(self, offer: Offer) -> Offer:
        session: Session = self.session_factory()
        try:
            model = OfferModel(
                id=generate_uuid(),
                post_id=offer.post_id,
                user_id=offer.user_id,
                description=offer.description,
                size=offer.size,
                fragile=offer.fragile,
                offer=offer.offer,
                created_at=offer.created_at,
            )
            session.add(model)
            session.commit()
            session.refresh(model)
            return _model_to_entity(model)
        finally:
            session.close()

    def get_by_id(self, offer_id: str) -> Optional[Offer]:
        session: Session = self.session_factory()
        try:
            model = session.query(OfferModel).filter(OfferModel.id == offer_id).first()
            return _model_to_entity(model) if model else None
        finally:
            session.close()

    def list(
        self,
        post_id: Optional[str] = None,
        owner_id: Optional[str] = None,
    ) -> List[Offer]:
        session: Session = self.session_factory()
        try:
            query = session.query(OfferModel)
            if post_id is not None:
                query = query.filter(OfferModel.post_id == post_id)
            if owner_id is not None:
                query = query.filter(OfferModel.user_id == owner_id)
            return [_model_to_entity(m) for m in query.all()]
        finally:
            session.close()

    def delete(self, offer_id: str) -> None:
        session: Session = self.session_factory()
        try:
            session.query(OfferModel).filter(OfferModel.id == offer_id).delete()
            session.commit()
        finally:
            session.close()

    def count(self) -> int:
        session: Session = self.session_factory()
        try:
            return session.query(func.count(OfferModel.id)).scalar() or 0
        finally:
            session.close()

    def reset(self) -> None:
        session: Session = self.session_factory()
        try:
            session.query(OfferModel).delete()
            session.commit()
        finally:
            session.close()
