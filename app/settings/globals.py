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
SECRET_KEY: str = config("SECRET_KEY", cast=str, default="foobar")
