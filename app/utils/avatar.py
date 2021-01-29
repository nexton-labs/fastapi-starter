import base64
import os
from datetime import datetime
from typing import Optional

from app.models.orm.user import User
from app.settings.globals import AWS_IMG_BUCKET, USER_AVATAR_PATH


def generate_user_avatar_path(user: User, filename: str) -> str:
    file_extension = os.path.splitext(filename)[1]
    ts = str(datetime.now().timestamp())
    ts_encoded = base64.urlsafe_b64encode(ts.encode()).rstrip(b"=").decode()
    return (
        USER_AVATAR_PATH.format(user_id=user.id, timestamp=ts_encoded) + file_extension
    )


def get_avatar_path_base64(avatar_path: Optional[str] = None) -> Optional[str]:
    if avatar_path:
        avatar_url = "s3://" + AWS_IMG_BUCKET + "/" + avatar_path
        encoded_url = (
            base64.urlsafe_b64encode(avatar_url.encode()).rstrip(b"=").decode()
        )
        return encoded_url

    return None
