import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.orm.base import ModelBase


class CandidateJobs(ModelBase):
    __tablename__ = "candidate_jobs"

    candidate_id = sa.Column(
        UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=False
    )
    job_id = sa.Column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False)

    candidate = relationship("Candidate", uselist=False)
    job = relationship("Job", uselist=False)  # type: ignore


class Candidate(ModelBase):
    __tablename__ = "candidates"

    user_id = sa.Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    linkedin_url = sa.Column(sa.String())

    jobs = relationship(
        "Job",
        secondary="candidate_jobs",
        primaryjoin="CandidateJobs.candidate_id==Candidate.id",
        secondaryjoin="CandidateJobs.job_id==Job.id",
    )  # type: ignore
    user = relationship("User", uselist=False)  # type: ignore
