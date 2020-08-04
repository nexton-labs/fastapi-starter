# type: ignore
from typing import List

from app.models.api.job import Job as JobDto, JobCreate

from app.db.session import Session
from app.repositories import job_repo


class JobService:
    def create(self, job: JobCreate, db: Session) -> JobDto:
        job = job_repo.create(db=db, obj_in=job)
        return JobDto.from_orm(job)

    def get_all(self, db: Session) -> List[JobDto]:
        return job_repo.find_multi(db=db)


job_service = JobService()
