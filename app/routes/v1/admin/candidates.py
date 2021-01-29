from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from app.cross.db import get_db
from app.db.session import Session
from app.models.api.candidate import (
    CandidateMinimal,
    CandidateDetails,
)
from app.models.api.user import UserInvitation, UserDetails
from app.services.api import candidate_service  # type: ignore

router = APIRouter()


@router.get("/", response_model=List[CandidateMinimal])
async def get_candidates(
    db: Session = Depends(get_db),  # type: ignore
):
    """Return user loaded candidates"""
    return candidate_service.get_all(db=db)


@router.get("/{candidate_id}/", response_model=CandidateDetails)
async def get_candidate_details(
    candidate_id: UUID, db: Session = Depends(get_db),  # type: ignore
):
    """Return user loaded candidates"""
    return candidate_service.get_details(db=db, candidate_id=candidate_id)


@router.post("/invitation", response_model=UserDetails)
async def invitation(
    data: UserInvitation, db: Session = Depends(get_db),  # type: ignore
):
    """
    ### Creates a new signup request for a user with PATIENT profile
    - Creates a new user for the given organization
    - Creates a user in Amazon Cognito (it will send a verification code)
    - Creates a new signup request with 'PENDING' status
    - Marks the user as disabled (not able to log into the application)

    Validations:

    Related screen:
    """
    return candidate_service.invite(db=db, data=data)


@router.post("/{candidate_id}/invitation/", response_model=UserDetails)
async def resend_invitation(
    candidate_id: UUID,
    data: UserInvitation,
    db: Session = Depends(get_db),  # type: ignore
):
    """
    ### Sends a new invitation email/phone to the patient using the same contact method than before
    - Marks the give invitation as REJECTED
    - Deletes the user in Amazon Cognito
    - Updates the user's email or phone number and those in the related patient.
    - Creates a new user in Amazon Cognito (it will send a temporary password)

    Validations:
    - An email or a phone number must be provided
    - The organization ID must be provided
    - The organization ID must exist

    Related screen:
    """

    return candidate_service.resend_invitation(
        db=db, candidate_id=candidate_id, data=data
    )


@router.post("/{candidate_id}/invitation_reminder/", response_model=UserDetails)
async def invitation_reminder(
    candidate_id: UUID, db: Session = Depends(get_db),  # type: ignore
):
    """
    ### Sends a new invitation email/phone to the patient using the same contact method than before
    - Marks the give invitation as REJECTED
    - Deletes the user in Amazon Cognito
    - Updates the user's email or phone number and those in the related patient.
    - Creates a new user in Amazon Cognito (it will send a temporary password)

    Validations:
    - An email or a phone number must be provided
    - The organization ID must be provided
    - The organization ID must exist

    Related screen:
    """

    return candidate_service.invitation_reminder(db=db, candidate_id=candidate_id)


@router.post("/{candidate_id}/jobs", response_model=CandidateDetails)
async def add_job(
    candidate_id: UUID,
    job_ids: List[UUID],
    db: Session = Depends(get_db),  # type: ignore
):
    """
    Associates a candidate to a job post
    """
    return candidate_service.add_jobs(db=db, candidate_id=candidate_id, job_ids=job_ids)


@router.delete("/{candidate_id}/jobs", response_model=CandidateDetails)
async def remove_job(
    candidate_id: UUID,
    job_ids: List[UUID],
    db: Session = Depends(get_db),  # type: ignore
):
    """
    Associates a candidate to a job post
    """
    return candidate_service.remove_jobs(
        db=db, candidate_id=candidate_id, job_ids=job_ids
    )
