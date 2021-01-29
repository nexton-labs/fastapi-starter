import random
import string
import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.models.orm.user import User


def build_user(
    db: Session,
    has_consented: Optional[bool] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
) -> User:

    username = random_email()
    if not email:
        email = username
    else:
        username = email
    if not phone:
        phone = random_lower_string()
    else:
        username = phone
    user = User(
        first_name=random_lower_string(),
        last_name=random_lower_string(),
        username=username,
        email=email,
        phone=phone,
        dob=sa.func.now(),
        gender="MALE",
    )
    if has_consented:
        user.has_consented = has_consented
        user.has_consented_date = datetime.utcnow()

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user(db: Session, user_id: UUID) -> Optional[User]:
    try:
        user: User = (db.query(User).get(user_id))
    except NoResultFound:
        return None

    return user


def generate_uuid() -> UUID:
    return uuid.uuid1()


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"
