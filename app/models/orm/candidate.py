import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.orm.base import ModelBase, RelationBase


class CandidateJobs(RelationBase):
    __tablename__ = "candidate_jobs"

    candidate_id = sa.Column(
        UUID(as_uuid=True), ForeignKey("candidates.id"), primary_key=True
    )
    job_id = sa.Column(UUID(as_uuid=True), ForeignKey("jobs.id"), primary_key=True)
    candidate = relationship("Candidate", back_populates="jobs")
    job = relationship("Job", back_populates="candidates")  # type: ignore


class Candidate(ModelBase):
    __tablename__ = "candidates"

    name = sa.Column(sa.String(), unique=False, nullable=False)
    email = sa.Column(sa.String(), unique=True, nullable=False)
    linkedin_url = sa.Column(sa.String(), unique=True, nullable=False)
    avatar_path = sa.Column(sa.String(), unique=True, nullable=True)
    jobs = relationship(CandidateJobs, back_populates="candidate")
    user_id = sa.Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="candidates")  # type: ignore
