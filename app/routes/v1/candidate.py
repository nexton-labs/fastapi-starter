from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Body

from app.db.session import Session
from app.models.api.candidate import Candidate as CandidateSchema, CandidateCreate
from app.cross.db import get_db
from app.cross import security as api_security
from app.services.api import candidate_service  # type: ignore


router = APIRouter()


@router.get("/", response_model=List[CandidateSchema])
async def get_candidates(
    db: Session = Depends(get_db),  # type: ignore
    user_id: str = Depends(api_security.get_auth_user_id),  # type: ignore
):
    """Return user loaded candidates"""
    return candidate_service.get_user_candidates(user_id=user_id, db=db)


@router.post("/", response_model=CandidateSchema)
async def create_candidate(
    db: Session = Depends(get_db),  # type: ignore
    user_id: str = Depends(api_security.get_auth_user_id),  # type: ignore
    candidate: CandidateCreate = Body(..., embed=True),
):
    """
    Stores a new candidate
    """
    return candidate_service.create(user_id=user_id, candidate=candidate, db=db)


@router.post("/{candidate_id}/job/{job_id}", response_model=CandidateSchema)
async def attach_job_post(
    candidate_id: UUID, job_id: UUID, db: Session = Depends(get_db),  # type: ignore
):
    """
    Associates a candidate to a job post
    """
    return candidate_service.add_job(candidate_id=candidate_id, job_id=job_id, db=db)
