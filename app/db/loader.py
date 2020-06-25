import importlib
import pkgutil

from app.models import orm


def load_models(mod=orm):
    for _, module_name, ispkg in pkgutil.walk_packages(mod.__path__):
        imod = importlib.import_module(f".{module_name}", mod.__name__)
        if ispkg:
            load_models(imod)
