import os
import logging
from logging.config import dictConfig
from typing import Optional, Dict


COV_TOKEN = os.environ.get("COV_TOKEN", "").strip() or None
COV_GIST_ID = os.environ.get("COV_GIST_ID", "").strip() or None
COV_FILENAME = os.environ.get("COV_FILENAME", "").strip() or None

URL_TEMPLATE = "https://datos.covid-19.conacyt.mx/Downloads/Files/Casos_Diarios_Estado_Nacional_Confirmados_{date}.csv"
URL_GIST = "https://gist.githubusercontent.com/RHDZMOTA/{gist_id}/raw/{filename}".format(
    gist_id=COV_GIST_ID,
    filename=COV_FILENAME
)

COV_DEFAULT_LOGLEVEL = os.environ.get(
    "COV_DEFAULT_LOGLEVEL",
    default="INFO"
).upper()

COV_DISABLE_EXISTING_LOGGERS = os.environ.get(
    "COV_DISABLE_EXISTING_LOGGERS",
    default="FALSE"
).upper().startswith("T")

logging_config = {
    "version": 1,
    "disable_existing_loggers": COV_DISABLE_EXISTING_LOGGERS,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "default": {
            "level": COV_DEFAULT_LOGLEVEL,
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": [
                "default"
            ],
            "level": COV_DEFAULT_LOGLEVEL,
            "propagate": True,
        }
    }
}


def get_logger(name: str, logging_config_dictionary: Optional[Dict] = None):
    if logging_config_dictionary is None:
        logging_config_dictionary = logging_config
    dictConfig(logging_config_dictionary)
    return logging.getLogger(name)
