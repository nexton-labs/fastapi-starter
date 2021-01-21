import logging
from configparser import RawConfigParser

import psycopg2.errors

from fastapi import FastAPI
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.db.loader import load_models
from app.db.session import Session
from app.repositories.exceptions import RecordNotFound
from app.utils.log import configure_logging


configure_logging()
load_models()

logger = logging.getLogger(__name__)

configParser = RawConfigParser()
configParser.read("setup.cfg")
version = configParser.get("metadata", "version", fallback="0.1.0")

app: FastAPI = FastAPI(
    title="FastAPI Nexton Starter", redoc_url="/redoc", version=version
)

# TODO: update this to be secure
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response


@app.exception_handler(IntegrityError)
async def sa_integrity_error(_, exc: IntegrityError):
    if exc.orig is not None:
        exc = exc.orig

    if isinstance(exc, psycopg2.errors.UniqueViolation):
        return JSONResponse(
            status_code=409,
            content={"detail": [{"msg": str(exc), "type": "unique_violation"}]},
        )
    elif isinstance(exc, psycopg2.errors.ExclusionViolation):
        return JSONResponse(
            status_code=409,
            content={
                "detail": [{"msg": str(exc), "type": "exclusion_violation"}]
            },  # "The request conflicts with existing resources."},
        )
    else:
        logger.error(exc)
        return JSONResponse(status_code=500, content={"detail": str(exc)})


@app.exception_handler(NoResultFound)
async def no_result_found_exception(_, __):
    return JSONResponse(status_code=404, content={"detail": "Not Found"})


@app.exception_handler(RecordNotFound)
async def record_not_found_exception(_, exc: RecordNotFound):
    return JSONResponse(status_code=404, content={"detail": str(exc.message)})


@app.exception_handler(Exception)
async def general_exception(_, exc: Exception):
    logger.error(exc)
    return JSONResponse(status_code=500, content={"detail": str(exc)})
