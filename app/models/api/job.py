from pydantic import BaseModel

from app.models.api.base import Base


class JobBase(Base):
    """
    Nexton job posting
    """

    title: str
    description: str


class JobCreate(BaseModel):
    title: str
    description: str


class JobUpdate(JobCreate):
    pass


class JobInDb(JobBase):
    pass


class Job(JobInDb):
    pass
