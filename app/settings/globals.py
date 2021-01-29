import sys
from pathlib import Path

from starlette.config import Config

_TESTING = "pytest" in sys.modules

p: Path
if _TESTING:
    p = Path(__file__).parents[2] / ".env.test"
else:
    p = Path(__file__).parents[2] / ".env"

config: Config
if p.exists():
    config = Config(str(p))
else:
    config = Config()

USER_AVATAR_PATH: str = "images/users/{user_id}/{user_id}_{timestamp}_avatar"
COGNITO_APP_CLIENT_ID: str = config(
    "COGNITO_APP_CLIENT_ID", cast=str, default="fake-app-client-id"
)
USER_PASSWORD_LENGTH: int = config("USER_PASSWORD_LENGTH", cast=int, default=10)
DEFAULT_IMAGE_FORMAT: str = config("DEFAULT_IMAGE_FORMAT", cast=str, default="webp")
IMAGE_PROXY_URL: str = config(
    "IMAGE_PROXY_URL", cast=str, default="d80a568d6g8mv.cloudfront.net",
)
IMAGE_PROXY_KEY: str = config("IMAGE_PROXY_KEY", cast=str, default="")
IMAGE_PROXY_SALT: str = config("IMAGE_PROXY_SALT", cast=str, default="")
TERMS_AND_CONDITIONS_PATH: str = config(
    "TERMS_AND_CONDITIONS_PATH", cast=str, default="static/terms_and_conditions.html"
)
DATABASE_URL: str = config("DATABASE_URL", cast=str, default="postgresql://")
COGNITO_POOL_ID: str = config("COGNITO_POOL_ID", cast=str, default="fake-pool-id")
COGNITO_REGION: str = config("COGNITO_REGION", cast=str, default="us-west-2")
CANDIDATE_AVATAR_PATH: str = "images/candidates/{candidate_id}/{candidate_id}_avatar"
AWS_IMG_BUCKET: str = config("AWS_IMG_BUCKET", cast=str, default="fastapi-starter")
MFA_ENABLED: bool = config("MFA_ENABLED", cast=bool, default="false")
