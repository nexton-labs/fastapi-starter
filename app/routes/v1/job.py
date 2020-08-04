from typing import List

from fastapi import APIRouter, Depends, Body

from app.db.session import Session
from app.models.api.job import Job as JobSchema
from app.models.api.job import JobCreate
from app.services.api import job_service  # type: ignore
from app.services.cross.db import get_db

router = APIRouter()


@router.get("/", response_model=List[JobSchema])
async def get_jobs(db: Session = Depends(get_db),):  # type: ignore
    """Return Nexton job posts"""
    return job_service.get_all(db=db)


@router.post("/", response_model=JobSchema)
async def create_job(
    job: JobCreate = Body(..., embed=True), db: Session = Depends(get_db),  # type: ignore
):
    """
    Stores a new job post
    """
    return job_service.create(db=db, job=job)
