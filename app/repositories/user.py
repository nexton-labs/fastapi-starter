# type: ignore
from app.models.api.user import UserCreate, UserUpdate
from app.models.orm.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    def update_user(self):
        print("unimplemented yet")


user_repo = UserRepository(User)
