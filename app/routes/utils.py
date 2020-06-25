import importlib
import typing

from fastapi import APIRouter
from fastapi.params import Depends as DependsType
from mypy_extensions import TypedDict

from app.models.api.util.exception import DataViolationError


class ResourcesDef(TypedDict):
    resources: typing.List[str]


class Namespace(ResourcesDef, total=False):
    dependencies: typing.Sequence[DependsType]


def get_module_routers(module_name: str) -> typing.Iterator[APIRouter]:
    api_module = importlib.import_module(module_name)

    for sub_router in api_module.__dict__.values():
        if isinstance(sub_router, APIRouter):
            yield sub_router


action_responses: typing.Dict[typing.Union[int, str], typing.Dict] = {
    409: {"model": DataViolationError},
}
