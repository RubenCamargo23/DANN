from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from adapters.database.route_model import RouteModel, generate_uuid
from domain.models.route import Route
from domain.ports.route_repository_port import RouteRepositoryPort


def _model_to_entity(model: RouteModel) -> Route:
    return Route(
        id=model.id,
        flight_id=model.flight_id,
        source_airport_code=model.source_airport_code,
        source_country=model.source_country,
        destiny_airport_code=model.destiny_airport_code,
        destiny_country=model.destiny_country,
        bag_cost=model.bag_cost,
        planned_start_date=model.planned_start_date,
        planned_end_date=model.planned_end_date,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


class SQLAlchemyRouteRepositoryAdapter(RouteRepositoryPort):
    """PostgreSQL implementation of RouteRepositoryPort using SQLAlchemy."""

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def create(self, route: Route) -> Route:
        session: Session = self.session_factory()
        try:
            model = RouteModel(
                id=generate_uuid(),
                flight_id=route.flight_id,
                source_airport_code=route.source_airport_code,
                source_country=route.source_country,
                destiny_airport_code=route.destiny_airport_code,
                destiny_country=route.destiny_country,
                bag_cost=route.bag_cost,
                planned_start_date=route.planned_start_date,
                planned_end_date=route.planned_end_date,
                created_at=route.created_at,
                updated_at=route.updated_at,
            )
            session.add(model)
            session.commit()
            session.refresh(model)
            return _model_to_entity(model)
        finally:
            session.close()

    def get_by_id(self, route_id: str) -> Optional[Route]:
        session: Session = self.session_factory()
        try:
            model = session.query(RouteModel).filter(RouteModel.id == route_id).first()
            return _model_to_entity(model) if model else None
        finally:
            session.close()

    def get_by_flight_id(self, flight_id: str) -> Optional[Route]:
        session: Session = self.session_factory()
        try:
            model = (
                session.query(RouteModel)
                .filter(RouteModel.flight_id == flight_id)
                .first()
            )
            return _model_to_entity(model) if model else None
        finally:
            session.close()

    def list(self, flight_id: Optional[str] = None) -> List[Route]:
        session: Session = self.session_factory()
        try:
            query = session.query(RouteModel)
            if flight_id:
                query = query.filter(RouteModel.flight_id == flight_id)
            return [_model_to_entity(m) for m in query.all()]
        finally:
            session.close()

    def delete(self, route_id: str) -> None:
        session: Session = self.session_factory()
        try:
            session.query(RouteModel).filter(RouteModel.id == route_id).delete()
            session.commit()
        finally:
            session.close()

    def count(self) -> int:
        session: Session = self.session_factory()
        try:
            return session.query(func.count(RouteModel.id)).scalar() or 0
        finally:
            session.close()

    def reset(self) -> None:
        session: Session = self.session_factory()
        try:
            session.query(RouteModel).delete()
            session.commit()
        finally:
            session.close()
