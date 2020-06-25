import typing

from pydantic import BaseModel
from pydantic import Field
from pydantic.generics import GenericModel


Item = typing.TypeVar("Item")
R = typing.TypeVar("R")


class ListMeta(BaseModel):
    """Pagination details about the result set"""

    total: int = Field(..., description="Total number of items in the result set")
    total_pages: int = Field(..., description="Total number of pages in the result set")
    page_size: int = Field(..., description="Number of items per page")
    page: int = Field(..., description="Page number to fetch")
    next_page: typing.Optional[int] = Field(None, description="Next page number")
    prev_page: typing.Optional[int] = Field(None, description="Previous page number")


class List(GenericModel, typing.Generic[Item]):
    """Response for returning a list of items, including a meta field for pagination"""

    meta: ListMeta
    data: typing.List[Item]

    class Config:
        arbitrary_types_allowed = True

    def fmap(self, f: typing.Callable[[Item], R]) -> "List[R]":
        return List[R](data=list(map(f, self.data)), meta=self.meta)


class Detail(GenericModel, typing.Generic[Item]):
    """Response for returning a single item"""

    data: Item
