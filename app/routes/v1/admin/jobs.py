from typing import List

from fastapi import APIRouter, Depends

from app.cross.db import get_db
from app.db.session import Session
from app.models.api.job import JobCreate, JobDetails
from app.services.api import job_service  # type: ignore

router = APIRouter()


@router.get("/", response_model=List[JobDetails])
async def get_jobs(db: Session = Depends(get_db),):  # type: ignore
    """Return Nexton job posts"""
    return job_service.get_all(db=db)


@router.post("/", response_model=JobDetails)
async def create_job(
    data: JobCreate, db: Session = Depends(get_db),  # type: ignore
):
    """
    Stores a new job post
    """
    return job_service.create(db=db, data=data)
