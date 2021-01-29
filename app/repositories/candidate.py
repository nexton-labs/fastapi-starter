from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.models.api.candidate import CandidateCreateDB, CandidateUpdateDB
from app.models.orm.candidate import Candidate, CandidateJobs
from app.models.orm.job import Job
from app.models.orm.user import User
from app.repositories.base import BaseRepository  # type: ignore


class CandidateRepository(
    BaseRepository[Candidate, CandidateCreateDB, CandidateUpdateDB]
):
    def create_candidate(
        self, db: Session, user_id: UUID, data: CandidateCreateDB,
    ) -> Candidate:
        db.begin_nested()
        candidate = Candidate(user_id=user_id, linkedin_url=data.linkedin_url)  # type: ignore

        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        return candidate

    def add_jobs(self, db: Session, candidate: Candidate, jobs: List[Job]) -> Candidate:
        db.begin_nested()

        for job in jobs:
            try:
                (
                    db.query(CandidateJobs)
                    .filter(CandidateJobs.candidate_id == candidate.id)
                    .filter(CandidateJobs.job_id == job.id)
                    .one()
                )
            except NoResultFound:
                candidate_job = CandidateJobs(candidate=candidate, job=job)
                db.add(candidate_job)

        db.commit()
        db.refresh(candidate)
        return candidate

    def remove_jobs(
        self, db: Session, candidate: Candidate, jobs: List[Job]
    ) -> Candidate:
        db.begin_nested()

        for job in jobs:  # type: ignore
            candidate.jobs.remove(job)  # type: ignore

        db.commit()
        db.refresh(candidate)
        return candidate

    def get_by_user(self, db: Session, user: User) -> Optional[Candidate]:
        try:
            candidate: Candidate = (
                db.query(Candidate).filter(Candidate.user_id == user.id).one()
            )
        except NoResultFound:
            return None

        return candidate


candidate_repo = CandidateRepository(Candidate)
