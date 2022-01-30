import datetime as dt
from typing import Optional, Tuple

import requests

from .settings import get_logger, URL_TEMPLATE


logger = get_logger(name=__name__)


def get_urls_generator(lag: int = 5):
    current_date = dt.datetime.utcnow()
    reference = current_date - dt.timedelta(days=lag)

    def recursive_closure():
        for i in range(lag + 1):
            date = (reference + dt.timedelta(days=i)).strftime("%Y%m%d")
            yield date, URL_TEMPLATE.format(date=date)

    return recursive_closure


def get_text(lag: int = 3) -> Optional[Tuple[str, str]]:
    urls_generator = get_urls_generator(lag=lag)
    latest_response = (None, None)
    for date, url in urls_generator():
        response = requests.get(url)
        if not response.ok:
            logger.debug("Dataset not found for date: %s", date)
            continue
        latest_response = (date, response.text)
    latest_date, _ = latest_response
    logger.info(f"Dataset found for date: {latest_date}")
    return latest_response
