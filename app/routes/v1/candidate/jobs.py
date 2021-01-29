from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from app.cross import security as api_security
from app.cross.db import get_db
from app.db.session import Session
from app.models.api.candidate import CandidateDetails
from app.models.orm.candidate import Candidate
from app.services.api import candidate_service  # type: ignore

router = APIRouter()


@router.post("/jobs", response_model=CandidateDetails)
async def add_job(
    job_ids: List[UUID],
    candidate: Candidate = Depends(api_security.get_auth_candidate),
    db: Session = Depends(get_db),  # type: ignore
):
    """
    Associates a candidate to a job post
    """
    return candidate_service.add_jobs(
        db=db,
        candidate_id=candidate.id,  # type: ignore
        job_ids=job_ids,
    )


@router.delete("/jobs", response_model=CandidateDetails)
async def remove_job(
    job_ids: List[UUID],
    candidate: Candidate = Depends(api_security.get_auth_candidate),
    db: Session = Depends(get_db),  # type: ignore
):
    """
    Associates a candidate to a job post
    """
    return candidate_service.remove_jobs(
        db=db,
        candidate_id=candidate.id,  # type: ignore
        job_ids=job_ids,
    )
