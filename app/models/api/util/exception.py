import typing

from pydantic import BaseModel


class ServerError(BaseModel):
    """Internal Server Error occurred."""

    detail: str = "Internal Server Error"


class DataError(BaseModel):
    msg: str
    type: str


class DataViolationError(BaseModel):
    """The data in the request conflicts with existing data."""

    detail: typing.List[DataError]


class NotFound(BaseModel):
    """A referenced model could not be found in the database."""

    detail: str = "Not Found"
