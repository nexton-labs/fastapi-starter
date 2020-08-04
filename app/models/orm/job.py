import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.models.orm.base import ModelBase
from app.models.orm.candidate import CandidateJobs


class Job(ModelBase):
    __tablename__ = "jobs"

    title = sa.Column(sa.String(), unique=True, nullable=False)
    description = sa.Column(sa.String(), unique=True, nullable=False)
    candidates = relationship(CandidateJobs, back_populates="job")
