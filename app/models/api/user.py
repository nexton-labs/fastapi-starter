from app.models.api.base import Base
from app.models.api.base import Field


class User(Base):
    """User account that can interact with API"""

    username: str = Field(..., description="Login name of user")
