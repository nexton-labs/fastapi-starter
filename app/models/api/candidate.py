from typing import Optional, List

from pydantic import BaseModel

from app.models.api.base import Field
from app.models.api.job import JobDetails
from app.models.api.user import UserDetails, UserMinimal
from app.models.orm.candidate import Candidate
from app.utils.avatar import get_avatar_path_base64


class CandidateDetails(UserDetails):
    """
    Nexton recruit candidate
    """

    linkedin_url: Optional[str] = Field(None, description="LinkedIn URL")
    jobs: List[JobDetails] = Field([], description="List of candidate jobs")

    @classmethod
    def from_model(cls, instance: Candidate):  # type: ignore
        return cls(
            id=instance.id,
            linkedin_url=instance.linkedin_url,
            first_name=instance.user.first_name,
            last_name=instance.user.last_name,
            username=instance.user.username,
            email=instance.user.email,
            phone=instance.user.phone,
            gender=instance.user.gender,
            dob=instance.user.dob,
            avatar_url=get_avatar_path_base64(instance.user.avatar_path),
            has_consented=instance.user.has_consented,
            has_consented_date=instance.user.has_consented_date,
            roles=[role.name for role in instance.user.roles],
            jobs=[JobDetails.from_model(job) for job in instance.jobs],
        )


class CandidateMinimal(UserMinimal):
    @classmethod
    def from_model(cls, instance: Candidate):
        return cls(
            id=instance.id,
            first_name=instance.user.first_name,
            last_name=instance.user.last_name,
            avatar_url=get_avatar_path_base64(instance.user.avatar_path),
        )


class CandidateCreateDB(BaseModel):
    linkedin_url: Optional[str] = Field(None, description="Candidate LinkedIn URL")


class CandidateUpdateDB(CandidateCreateDB):
    pass
