# type: ignore
from uuid import UUID

from app.db.session import Session
from app.models.api.job import JobCreate, JobUpdate
from app.models.orm.candidate import Candidate, CandidateJobs
from app.models.orm.job import Job
from app.repositories.base import BaseRepository


class JobRepository(BaseRepository[Job, JobCreate, JobUpdate]):
    def attach_job_to_candidate(
        self, candidate: Candidate, job_id: UUID, db: Session
    ) -> Job:
        db_job = self.find(db=db, model_id=job_id)

        db_candidates_jobs = CandidateJobs()
        db_candidates_jobs.candidate = candidate
        db_job.candidates.append(db_candidates_jobs)

        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        return db_job


job_repo = JobRepository(Job)
