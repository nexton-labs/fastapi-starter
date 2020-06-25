from fastapi import APIRouter

from app.models.api.util.health import Health


router = APIRouter()


@router.get("/health", tags=["System"], response_model=Health)
def healthcheck():
    """Returns health status for system. Typically returns `OK`."""
    return Health()
