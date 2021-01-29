from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.models.api.user import UserCreateDB, UserUpdateDB
from app.models.orm.user import User, Role, UserRole
from app.repositories.base import BaseRepository  # type: ignore


class UserRepository(BaseRepository[User, UserCreateDB, UserUpdateDB]):
    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        try:
            user: User = (db.query(User).filter(User.username == username).one())
        except NoResultFound:
            return None

        return user

    def add_role(self, db: Session, user: User, role: Role) -> User:
        db.begin_nested()

        try:
            (
                db.query(UserRole)
                .filter(UserRole.user_id == user.id)
                .filter(UserRole.role_id == role.id)
                .one()
            )
        except NoResultFound:
            user_role = UserRole(user=user, role=role)
            db.add(user_role)

            db.commit()
            db.refresh(user)

        return user

    def remove_role(self, db: Session, user: User, role: Role) -> User:
        db.begin_nested()

        try:
            user_role: UserRole = (
                db.query(UserRole)
                .filter(UserRole.user_id == user.id)
                .filter(UserRole.role_id == role.id)
                .one()
            )
        except NoResultFound:
            return user

        user.roles.remove(user_role.role)  # type: ignore
        db.add(user)

        db.commit()
        db.refresh(user)

        return user


user_repo = UserRepository(User)
