from app.models.api.base import Base


class UserBase(Base):
    """
    Nexton user
    """

    username: str
    email: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass
