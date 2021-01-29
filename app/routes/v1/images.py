from fastapi import APIRouter

from app.settings.globals import IMAGE_PROXY_URL, DEFAULT_IMAGE_FORMAT
from app.utils.constants import ImageSize
from app.utils.url_signature import url_signature

router = APIRouter()

# https://docs.imgproxy.net/#/generating_the_url_advanced
IMG_PATH_TEMPLATE = "/rs:fill:{size}:0:0/g:sm/{path}." + DEFAULT_IMAGE_FORMAT
IMG_RRL_TEMPLATE = "https://{proxy_url}/{signed_path}"


@router.get("/{image_path}", response_model=str)
async def get_resized_image(image_path: str, image_size: ImageSize):
    """
    Retrieves a signed URL with the processing options.
    """
    # https://docs.imgproxy.net/#/signing_the_url
    processing_options = IMG_PATH_TEMPLATE.format(
        size=ImageSize.get_size(image_size), path=image_path
    )
    signed_path = url_signature.sign_path(processing_options)
    return IMG_RRL_TEMPLATE.format(proxy_url=IMAGE_PROXY_URL, signed_path=signed_path)
