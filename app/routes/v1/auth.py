from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.api.user import User as UserSchema
from app.models.api.util.tokens import Token
from app.models.orm.user import User
from app.services import security
from app.services.api import security as api_security
from app.services.api.db import get_db


router = APIRouter()


@router.get("/me", response_model=UserSchema)
async def get_me(user: User = Depends(api_security.get_current_user)):
    """Returns the authenticated user"""
    return UserSchema.from_orm(user)


@router.post(api_security.TOKEN_URL, response_model=Token)
async def get_token(
    db: Session = Depends(get_db),
    form_data: api_security.OAuth2SecretPasswordRequestForm = Depends(),
):
    """Returns Bearer token for authentication for other endpoints

    Utilizes OAuth2 Password Grant Flow only.
    """
    user = security.authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect name or password")

    return api_security.vend_token(user)
