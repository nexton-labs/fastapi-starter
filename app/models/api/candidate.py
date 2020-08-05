from pydantic import BaseModel

from app.models.api.base import Base
from app.models.api.base import Field


class CandidateBase(Base):
    """
    Nexton recruit candidate
    """

    name: str = Field(..., description="Candidate name")
    email: str = Field(..., description="Candidate email")
    linkedin_url: str = Field(..., description="LinkedIn URL")


class CandidateCreate(BaseModel):
    name: str = Field(..., description="Candidate name")
    email: str = Field(..., description="Candidate email")
    linkedin_url: str = Field(..., description="LinkedIn URL")


class CandidateUpdate(CandidateCreate):
    pass


class CandidateInDb(CandidateBase):
    pass


class Candidate(CandidateInDb):
    pass
