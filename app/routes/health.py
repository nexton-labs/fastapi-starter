from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.cross.db import get_db
from app.models.api.util.health import Health
from app.repositories.base import get_version  # type: ignore

router = APIRouter()


@router.get("/health", tags=["System"], response_model=Health)
def healthcheck(db: Session = Depends(get_db)):
    """Returns health status for system. Typically returns `OK`."""
    try:
        db_version = get_version(db)
        return Health(db_version=db_version)
    except SQLAlchemyError as ex:
        return Health(status="ERROR", status_description=str(ex))
