import typing

from pydantic import SecretStr
from sqlalchemy.orm import Session

from app.models.orm.user import User
from app.services import password


def authenticate_user(
    db: Session, username: str, given_password: SecretStr
) -> typing.Optional[User]:
    user: User = db.query(User).filter(User.username == username).first()

    if user is None:
        return None

    if not password.verify(given_password, user.hashed_password):
        return None

    return user
