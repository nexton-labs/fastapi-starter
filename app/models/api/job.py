from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.orm.job import Job


class JobDetails(BaseModel):
    id: UUID = Field(..., description="Job identifier")
    title: str = Field(..., description="Job title", example="Software developer")
    description: Optional[str] = Field(
        None, description="Job description", example="Software developer"
    )

    @classmethod
    def from_model(cls, instance: Job):
        return cls(
            id=instance.id, title=instance.title, description=instance.description,
        )


class JobCreate(BaseModel):
    title: str = Field(..., description="Job title", example="Software developer")
    description: Optional[str] = Field(
        None, description="Job description", example="Software developer"
    )


class JobUpdate(BaseModel):
    title: Optional[str] = Field(
        None, description="Job title", example="Software developer"
    )
    description: Optional[str] = Field(
        None, description="Job description", example="Software developer"
    )
