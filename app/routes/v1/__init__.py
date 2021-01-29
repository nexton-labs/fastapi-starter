import logging
import typing

from fastapi import APIRouter, Depends

from app.cross import security as api_security
from app.models.api.util.exception import NotFound, ServerError
from app.routes.utils import Namespace, get_module_routers

logger = logging.getLogger(__name__)


def get_router() -> APIRouter:
    router = APIRouter()

    namespaces: typing.Dict[str, Namespace] = {
        "admin": {
            "resources": ["admin/candidates", "admin/jobs", "admin/users"],
            # "dependencies": [Depends(api_security.get_auth_admin)],  # type: ignore
        },
        "candidate": {
            "resources": ["candidate/jobs", "candidate/users"],
            "dependencies": [Depends(api_security.get_auth_candidate)],  # type: ignore
        },
        "anonymous": {"resources": ["images", "files", "signup"]},
    }

    for name, namespace in namespaces.items():
        logger.debug("Mounting namespace: %s", name)
        for resource in namespace["resources"]:
            module_name = f"app.routes.v1.{resource.replace('/', '.')}"
            logger.debug("\tMounting %s", module_name)
            for sub_router in get_module_routers(module_name):
                router.include_router(
                    sub_router,
                    prefix=f"/{resource}",
                    tags=[resource.replace("/", " -> ").capitalize()],
                    dependencies=namespace.get("dependencies", []),
                    responses={500: {"model": ServerError}, 404: {"model": NotFound}},
                )

    return router
