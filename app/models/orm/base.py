import typing

import sqlalchemy as sa

from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base


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


class RelationBase(Base):
    __abstract__ = True

    created_at = sa.Column(sa.DateTime, server_default=sa.func.now(), nullable=False)
    updated_at = sa.Column(
        sa.DateTime,
        onupdate=sa.func.now(),
        server_default=sa.func.now(),
        nullable=False,
    )
