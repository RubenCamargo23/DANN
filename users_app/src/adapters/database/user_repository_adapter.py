from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from adapters.database.user_model import UserModel, generate_uuid
from domain.models.user import User
from domain.ports.user_repository_port import UserRepositoryPort


def _model_to_entity(model: UserModel) -> User:
    return User(
        id=model.id,
        username=model.username,
        email=model.email,
        phone_number=model.phone_number,
        dni=model.dni,
        full_name=model.full_name,
        password=model.password,
        salt=model.salt,
        token=model.token,
        status=model.status,
        expire_at=model.expire_at,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


class SQLAlchemyUserRepositoryAdapter(UserRepositoryPort):
    """PostgreSQL implementation of UserRepositoryPort using SQLAlchemy."""

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def create(self, user: User) -> User:
        session: Session = self.session_factory()
        try:
            model = UserModel(
                id=generate_uuid(),
                username=user.username,
                email=user.email,
                phone_number=user.phone_number,
                dni=user.dni,
                full_name=user.full_name,
                password=user.password,
                salt=user.salt,
                status=user.status,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
            session.add(model)
            session.commit()
            session.refresh(model)
            return _model_to_entity(model)
        finally:
            session.close()

    def get_by_id(self, user_id: str) -> Optional[User]:
        session: Session = self.session_factory()
        try:
            model = session.query(UserModel).filter(UserModel.id == user_id).first()
            return _model_to_entity(model) if model else None
        finally:
            session.close()

    def get_by_username(self, username: str) -> Optional[User]:
        session: Session = self.session_factory()
        try:
            model = (
                session.query(UserModel)
                .filter(UserModel.username == username)
                .first()
            )
            return _model_to_entity(model) if model else None
        finally:
            session.close()

    def get_by_username_or_email(self, username: str, email: str) -> Optional[User]:
        session: Session = self.session_factory()
        try:
            model = (
                session.query(UserModel)
                .filter(
                    (UserModel.username == username) | (UserModel.email == email)
                )
                .first()
            )
            return _model_to_entity(model) if model else None
        finally:
            session.close()

    def get_by_token(self, token: str) -> Optional[User]:
        session: Session = self.session_factory()
        try:
            model = session.query(UserModel).filter(UserModel.token == token).first()
            return _model_to_entity(model) if model else None
        finally:
            session.close()

    def update(self, user: User) -> User:
        session: Session = self.session_factory()
        try:
            model = session.query(UserModel).filter(UserModel.id == user.id).first()
            model.status = user.status
            model.dni = user.dni
            model.full_name = user.full_name
            model.phone_number = user.phone_number
            model.token = user.token
            model.expire_at = user.expire_at
            model.updated_at = user.updated_at
            session.commit()
            session.refresh(model)
            return _model_to_entity(model)
        finally:
            session.close()

    def count(self) -> int:
        session: Session = self.session_factory()
        try:
            return session.query(func.count(UserModel.id)).scalar() or 0
        finally:
            session.close()

    def reset(self) -> None:
        session: Session = self.session_factory()
        try:
            session.query(UserModel).delete()
            session.commit()
        finally:
            session.close()
