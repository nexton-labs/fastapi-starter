from typing import List

from sqlalchemy.orm import Session

from app.models.api.job import JobCreate, JobDetails
from app.repositories import job_repo


class JobService:
    def create(self, data: JobCreate, db: Session) -> JobDetails:
        job = job_repo.create(db=db, obj_in=data)
        job_schema: JobDetails = JobDetails.from_model(job)
        return job_schema

    def get_all(self, db: Session) -> List[JobDetails]:
        jobs_schema: List[JobDetails] = []
        jobs = job_repo.find_multi(db=db)
        for job in jobs:
            jobs_schema.append(JobDetails.from_model(job))

        return jobs_schema


job_service = JobService()
