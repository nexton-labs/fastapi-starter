import typing
import uuid

import sqlalchemy as sa

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.db.base_class import Base
from app.models.orm.exceptions import RecordNotFound


M = typing.TypeVar("M", bound="ModelBase")


class ModelBase(Base):
    __abstract__ = True
    id = sa.Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=sa.text("uuid_generate_v4()"),
    )

    created_at = sa.Column(sa.DateTime, server_default=sa.func.now(), nullable=False)
    updated_at = sa.Column(
        sa.DateTime,
        onupdate=sa.func.now(),
        server_default=sa.func.now(),
        nullable=False,
    )

    @classmethod
    def find(cls: typing.Type[M], db: Session, model_id: uuid.UUID) -> M:
        try:
            model: M = db.query(cls).filter(cls.id == model_id).one()
        except NoResultFound:
            raise RecordNotFound(cls, model_id)

        return model
