import sqlalchemy as sa

from app.models.orm.base import ModelBase


class User(ModelBase):
    __tablename__ = "users"

    username = sa.Column(sa.String(), unique=True, nullable=False)
    hashed_password = sa.Column(sa.String(), nullable=False)
