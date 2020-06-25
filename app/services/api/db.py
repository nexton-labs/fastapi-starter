from sqlalchemy.orm import Session
from starlette.requests import Request


def get_db(request: Request) -> Session:
    return request.state.db  # type: ignore
