from pathlib import Path

from starlette.config import Config

from app.utils import _TESTING


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

DATABASE_URL: str = config("DATABASE_URL", cast=str, default="postgresql://")
COGNITO_POOL_ID: str = config("COGNITO_POOL_ID", cast=str, default="fake-pool-id")
COGNITO_REGION: str = config("COGNITO_REGION", cast=str, default="us-west-2")
CANDIDATE_AVATAR_PATH: str = "images/candidates/{candidate_id}/{candidate_id}_avatar"
AWS_IMG_BUCKET: str = config("AWS_IMG_BUCKET", cast=str, default="fastapi-starter")
AWS_ACCESS_KEY_ID: str = config(
    "AWS_ACCESS_KEY_ID", cast=str, default="DUMMY_AWS_ACCESS_KEY_ID"
)
AWS_SECRET_ACCESS_KEY: str = config(
    "AWS_SECRET_ACCESS_KEY", cast=str, default="DUMMY_AWS_ACCESS_KEY_ID"
)
