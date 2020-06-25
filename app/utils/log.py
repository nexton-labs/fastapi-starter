import logging.config


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "format": "{levelprefix} {asctime} - {name}:{lineno} - {message}",
            "style": "{",
            "use_colors": None,
        },
        "print": {
            "()": "uvicorn.logging.DefaultFormatter",
            "format": "SQL: {message}",
            "style": "{",
            "use_colors": None,
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "print": {
            "formatter": "print",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "app": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "sqlalchemy.engine": {
            "handlers": ["print"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


def configure_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
    logging.getLogger("livereload").propagate = False
