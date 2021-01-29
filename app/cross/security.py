from typing import List, Dict, Optional
from uuid import UUID

import requests
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, jwk, JWTError
from jose.utils import base64url_decode
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN

from app.cross.db import get_db
from app.models.orm.candidate import Candidate
from app.models.orm.user import User
from app.repositories import user_repo, candidate_repo
from app.settings.globals import COGNITO_POOL_ID, COGNITO_REGION
from app.utils.constants import Role

JWK = Dict[str, str]


class JWKS(BaseModel):
    keys: List[JWK]


json_web_key_set = JWKS.parse_obj(
    requests.get(
        f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/"
        f"{COGNITO_POOL_ID}/.well-known/jwks.json"
    ).json()
)


class JWTAuthorizationCredentials(BaseModel):
    jwt_token: str
    header: Dict[str, str]
    claims: Dict[str, str]
    signature: str
    message: str


class JWTBearer(HTTPBearer):
    def __init__(self, jwks: JWKS, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

        self.kid_to_jwk = {jwk["kid"]: jwk for jwk in jwks.keys}

    def verify_jwk_token(self, jwt_credentials: JWTAuthorizationCredentials) -> bool:
        try:
            public_key = self.kid_to_jwk[jwt_credentials.header["kid"]]
        except KeyError:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="JWK public key not found"
            )

        key = jwk.construct(public_key)
        decoded_signature = base64url_decode(jwt_credentials.signature.encode())

        is_valid: bool = key.verify(jwt_credentials.message.encode(), decoded_signature)
        return is_valid

    async def __call__(self, request: Request) -> Optional[JWTAuthorizationCredentials]:  # type: ignore
        credentials: Optional[HTTPAuthorizationCredentials] = await super().__call__(
            request
        )

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Wrong authentication method"
                )

            jwt_token = credentials.credentials

            message, signature = jwt_token.rsplit(".", 1)

            try:
                jwt_credentials = JWTAuthorizationCredentials(
                    jwt_token=jwt_token,
                    header=jwt.get_unverified_header(jwt_token),
                    claims=jwt.get_unverified_claims(jwt_token),
                    signature=signature,
                    message=message,
                )
            except JWTError:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="JWK invalid"
                )

            if not self.verify_jwk_token(jwt_credentials):
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="JWK invalid"
                )

            return jwt_credentials
        return None


auth = JWTBearer(json_web_key_set)


async def get_auth_user_id(
    credentials: JWTAuthorizationCredentials = Depends(auth),
) -> str:
    try:
        return credentials.claims["custom:id"]
    except KeyError:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="ID missing")


async def get_auth_user(
    db: Session = Depends(get_db), user_id: UUID = Depends(get_auth_user_id),
) -> Optional[User]:
    user: User = user_repo.find(db=db, model_id=user_id)
    return user


async def get_auth_admin(user: User = Depends(get_auth_user),) -> User:
    if Role.ADMIN.name not in [role.name for role in user.roles]:  # type: ignore
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="User is not admin")
    return user


async def get_auth_candidate(
    db: Session = Depends(get_db), user: User = Depends(get_auth_user),
) -> Optional[Candidate]:
    if Role.CANDIDATE.name not in [role.name for role in user.roles]:  # type: ignore
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="User is not a candidate"
        )
    candidate = candidate_repo.get_by_user(db=db, user=user)
    return candidate
