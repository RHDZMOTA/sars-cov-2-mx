import logging
from typing import Optional

import requests
import pandas as pd

from .utils import get_text
from .settings import URL_GIST


logger = logging.getLogger(__name__)


def parse_text(string: str) -> Optional[pd.DataFrame]:
    try:
        header, *records = [row.split(",") for row in string.splitlines()]
        return pd.DataFrame(records, columns=header)
    except Exception as e:
        logger.warning("Exception found when parsing the text: %s", str(e))


def get_latest_data(lag: int = 5) -> Optional[pd.DataFrame]:
    """Get data from the official MX Sources (can be None if not found in the latest days)"""
    text = get_text(lag=lag)
    if not text:
        return
    return parse_text(string=text)


def get_latest_snapshot() -> Optional[pd.DataFrame]:
    response = requests.get(URL_GIST)
    if not response.ok:
        return
    return parse_text(string=response.text)
