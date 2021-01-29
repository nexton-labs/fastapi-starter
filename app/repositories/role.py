from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.models.orm.user import Role
from app.repositories.base import BaseRepository  # type: ignore


class RoleRepository(BaseRepository[Role, None, None]):
    def get_by_name(self, db: Session, name: str) -> Optional[Role]:
        try:
            role: Role = (db.query(Role).filter(Role.name == name).one())
            return role
        except NoResultFound:
            return None


role_repo = RoleRepository(Role)
