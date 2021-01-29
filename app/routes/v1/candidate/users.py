from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.cross import security as api_security
from app.cross.db import get_db
from app.models.api.user import UserDetails
from app.models.orm.candidate import Candidate
from app.services.api import user_service  # type: ignore

router = APIRouter()


@router.get("/profile/", response_model=UserDetails)
async def get_profile(
    candidate: Candidate = Depends(api_security.get_auth_candidate),
    db: Session = Depends(get_db),  # type: ignore
):
    """
    Retrieves user details.
    """

    return user_service.get_profile(db=db, user=candidate.user)


@router.post("/avatar/", response_model=str)
async def set_avatar(
    candidate: Candidate = Depends(api_security.get_auth_candidate),
    file: UploadFile = File(...),  # type: ignore
    db: Session = Depends(get_db),
):
    """
    Uploads the candidate's avatar image and saves the path.
    """
    return user_service.set_avatar(db=db, user=candidate.user, file=file)
