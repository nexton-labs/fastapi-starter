from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.cross.db import get_db
from app.models.api.user import UserDetails, UserSignup
from app.services.api import candidate_service  # type: ignore

router = APIRouter()


@router.post("/signup", response_model=UserDetails)
async def signup(
    data: UserSignup, db: Session = Depends(get_db),  # type: ignore
):
    """
    ### Creates a new signup request for a user
    - Creates a user in Amazon Cognito (it will send a verification code)
    - Marks the user as disabled (not able to log into the application)

    Validations:

    Related screen:
    """
    return candidate_service.signup(db=db, data=data)
