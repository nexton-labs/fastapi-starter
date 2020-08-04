import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.models.orm.base import ModelBase


class User(ModelBase):
    __tablename__ = "users"

    username = sa.Column(sa.String(), unique=True, nullable=False)
    email = sa.Column(sa.String(), unique=True, nullable=False)
    candidates = relationship("Candidate", back_populates="user")  # type: ignore
