import multiprocessing
import os
import typing

import gunicorn.app.base
import uvicorn.workers
from starlette.applications import Starlette


def number_of_workers() -> int:
    return multiprocessing.cpu_count() + 1


class StandaloneApplication(gunicorn.app.base.BaseApplication):
    # pylint: disable=abstract-method

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


class LifespanUvicornWorker(uvicorn.workers.UvicornWorker):
    CONFIG_KWARGS = {"loop": "uvloop", "http": "httptools", "lifespan": "on"}


def run(app: Starlette, options: typing.Optional[dict] = None):
    if options is None:
        options = {}

    default_options = {
        "bind": "%s:%s" % ("0.0.0.0", os.environ.get("PORT", "8080")),
        "workers": number_of_workers(),
        "worker_class": "app.server.LifespanUvicornWorker",
        "threads": 2,
        "capture_output": True,
    }

    return StandaloneApplication(app, {**default_options, **options}).run()


def debug(app: Starlette):
    uvicorn.run(app, host="0.0.0.0", port=8000)
