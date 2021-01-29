import sqlalchemy as sa
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.orm.base import ModelBase
from app.utils.constants import Gender

gender_enum = ENUM(*Gender.list(), name="gender", createType=False)


class User(ModelBase):
    __tablename__ = "users"

    first_name = sa.Column(sa.String(), nullable=False)
    last_name = sa.Column(sa.String(), nullable=False)
    dob = sa.Column(sa.DateTime)
    gender = sa.Column(gender_enum)
    username = sa.Column(sa.String(), unique=True, nullable=False)
    email = sa.Column(sa.String())
    phone = sa.Column(sa.String())
    has_consented = sa.Column(sa.Boolean, server_default="f", nullable=False)
    has_consented_date = sa.Column(sa.DateTime)
    avatar_path = sa.Column(sa.String())

    roles = relationship(
        "Role",
        secondary="user_roles",
        primaryjoin="UserRole.user_id==User.id",
        secondaryjoin="UserRole.role_id==Role.id",
    )  # type: ignore


class Role(ModelBase):
    __tablename__ = "roles"

    name = sa.Column(sa.String(), unique=True, nullable=False)
    description = sa.Column(sa.String())

    users = relationship(
        "User",
        secondary="user_roles",
        primaryjoin="UserRole.role_id==Role.id",
        secondaryjoin="UserRole.user_id==User.id",
    )  # type: ignore


class UserRole(ModelBase):
    __tablename__ = "user_roles"

    user_id = sa.Column(UUID(as_uuid=True), ForeignKey("users.id"))
    role_id = sa.Column(UUID(as_uuid=True), ForeignKey("roles.id"))

    user = relationship(User, uselist=False)
    role = relationship(Role, uselist=False)

    __table_args__ = (
        UniqueConstraint("user_id", "role_id", name="_customer_location_uc"),
    )
