import datetime
import typing
import uuid

import fastapi.security
import jwt

from fastapi import Depends
from fastapi import HTTPException
from fastapi.param_functions import Form
from pydantic import SecretStr
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from app.models.api.util.tokens import Token
from app.models.orm.user import User
from app.services.api.db import get_db
from app.settings.globals import SECRET_KEY


ALGORITHM = "HS256"
TOKEN_URL = "/token"
oauth2_scheme = fastapi.security.OAuth2PasswordBearer(tokenUrl=f"/v1/auth{TOKEN_URL}")
# TODO: Change this to 30
ACCESS_TOKEN_EXPIRE_MINUTES = 3600


def create_access_token(
    *, data: dict, expires_delta: typing.Optional[datetime.timedelta] = None
) -> bytes:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def vend_token(user: User) -> Token:
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return Token(access_token=access_token, token_type="bearer")


async def decode_token(db: Session, token: str) -> typing.Optional[User]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except (jwt.ExpiredSignatureError, jwt.DecodeError):
        return None

    sub = payload.get("sub")
    if not isinstance(sub, str):
        return None

    return User.find(db, uuid.UUID(sub))


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    user = await decode_token(db, token)

    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


class OAuth2SecretPasswordRequestForm:
    """
    Based on fastapi.security.tf.OAuth2PasswordRequestForm but,
        with password being a SecretStr
    """

    def __init__(
        self,
        grant_type: str = Form(
            None,
            regex="password",
            description="Specifies OAuth2 grant type; accepts only `password`.",
        ),
        username: str = Form(..., description="Login name of user"),
        password: SecretStr = Form(..., description="Password of user"),
        scope: str = Form(
            "", description="Scope of OAuth2 grant; unused in this implementation"
        ),
        client_id: typing.Optional[str] = Form(
            None, description="Client ID of authenticating application; unused."
        ),
        client_secret: typing.Optional[str] = Form(
            None, description="Client Secret of authenticating application; unused."
        ),
    ):
        self.grant_type = grant_type
        self.username = username
        self.password = password
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret
