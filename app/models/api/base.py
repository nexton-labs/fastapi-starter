import datetime

from uuid import UUID

from pydantic import BaseModel
from pydantic import Field


class Base(BaseModel):
    id: UUID = Field(..., description="The identifier for this data model")
    created_at: datetime.datetime = Field(
        ..., description="The datetime when this data model was created"
    )
    updated_at: datetime.datetime = Field(
        ..., description="The datetime when this data model was last updated"
    )

    @classmethod
    def from_dict(cls, kwargs) -> "Base":
        return cls(**kwargs)

    class Config:
        orm_mode = True
