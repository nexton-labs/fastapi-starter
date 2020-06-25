"Startup commands to make it easier to use iPython for dev"

# flake8: noqa
# pylint: skip-file

import sqlalchemy as sa

from app.db.loader import load_models
from app.db.session import Session


load_models()
db = Session()
