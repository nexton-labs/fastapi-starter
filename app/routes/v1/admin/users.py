from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.cross.db import get_db
from app.models.api.user import UserDetails, UserSignup
from app.services.api import user_service  # type: ignore

router = APIRouter()


@router.post("/admin", response_model=UserDetails)
async def create_admin(
    data: UserSignup, db: Session = Depends(get_db),  # type: ignore
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
    return user_service.create_admin(db=db, data=data)
