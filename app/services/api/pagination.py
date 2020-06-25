import math
import typing

from fastapi import Query
from pydantic import BaseModel
from sqlalchemy.orm.query import Query as SAQuery

from app.models.api.util.response import List
from app.models.api.util.response import ListMeta
from app.models.orm.base import ModelBase


T = typing.TypeVar("T", bound=ModelBase)


class Paginate(BaseModel):
    page: int = Query(1, ge=1, description="Page number to fetch")
    page_size: int = Query(10, ge=1, le=1000, description="Number of items per page")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    def total_pages(self, count) -> int:
        return math.ceil(count * 1.0 / self.page_size)

    def next_page(self, total) -> typing.Optional[int]:
        if self.page_size * self.page >= total:
            return None
        return self.page + 1

    @property
    def prev_page(self) -> typing.Optional[int]:
        if self.page == 1:
            return None
        return self.page - 1

    def __call__(self, scope: SAQuery) -> List[T]:
        total = scope.count()

        results = scope.limit(self.page_size).offset(self.offset).all()

        meta = ListMeta(
            total=total,
            total_pages=self.total_pages(total),
            page_size=self.page_size,
            page=self.page,
            next_page=self.next_page(total),
            prev_page=self.prev_page,
        )

        return List(data=results, meta=meta)
