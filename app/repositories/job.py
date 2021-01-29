from app.models.api.job import JobCreate, JobUpdate
from app.models.orm.job import Job
from app.repositories.base import BaseRepository  # type: ignore


class JobRepository(BaseRepository[Job, JobCreate, JobUpdate]):
    pass


job_repo = JobRepository(Job)
