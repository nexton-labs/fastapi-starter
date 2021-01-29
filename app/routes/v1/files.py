from fastapi import APIRouter

from app.settings.globals import (
    TERMS_AND_CONDITIONS_PATH,
    AWS_IMG_BUCKET,
)
from app.utils.s3_management import s3_management

router = APIRouter()


@router.post("/terms_and_conditions/", response_model=str)
async def get_terms_and_conditions():
    """
    ### Returns a presigned URL to download Terms and Conditions file

    Related screen:
    """
    return s3_management.generate_presigned_url(
        TERMS_AND_CONDITIONS_PATH, AWS_IMG_BUCKET, 86400  # 1 day
    )
