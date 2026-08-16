from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from adapters.database.post_model import PostModel, generate_uuid
from domain.models.post import Post
from domain.ports.post_repository_port import PostRepositoryPort


def _model_to_entity(model: PostModel) -> Post:
    return Post(
        id=model.id,
        route_id=model.route_id,
        user_id=model.user_id,
        expire_at=model.expire_at,
        created_at=model.created_at,
    )


class SQLAlchemyPostRepositoryAdapter(PostRepositoryPort):
    """PostgreSQL implementation of PostRepositoryPort using SQLAlchemy."""

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def create(self, post: Post) -> Post:
        session: Session = self.session_factory()
        try:
            model = PostModel(
                id=generate_uuid(),
                route_id=post.route_id,
                user_id=post.user_id,
                expire_at=post.expire_at,
                created_at=post.created_at,
            )
            session.add(model)
            session.commit()
            session.refresh(model)
            return _model_to_entity(model)
        finally:
            session.close()

    def get_by_id(self, post_id: str) -> Optional[Post]:
        session: Session = self.session_factory()
        try:
            model = session.query(PostModel).filter(PostModel.id == post_id).first()
            return _model_to_entity(model) if model else None
        finally:
            session.close()

    def list(
        self,
        route_id: Optional[str] = None,
        owner_id: Optional[str] = None,
    ) -> List[Post]:
        session: Session = self.session_factory()
        try:
            query = session.query(PostModel)
            if route_id is not None:
                query = query.filter(PostModel.route_id == route_id)
            if owner_id is not None:
                query = query.filter(PostModel.user_id == owner_id)
            return [_model_to_entity(m) for m in query.all()]
        finally:
            session.close()

    def delete(self, post_id: str) -> None:
        session: Session = self.session_factory()
        try:
            session.query(PostModel).filter(PostModel.id == post_id).delete()
            session.commit()
        finally:
            session.close()

    def count(self) -> int:
        session: Session = self.session_factory()
        try:
            return session.query(func.count(PostModel.id)).scalar() or 0
        finally:
            session.close()

    def reset(self) -> None:
        session: Session = self.session_factory()
        try:
            session.query(PostModel).delete()
            session.commit()
        finally:
            session.close()
