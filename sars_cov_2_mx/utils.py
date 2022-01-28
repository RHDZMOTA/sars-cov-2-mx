import datetime as dt
from typing import Optional

import requests

from .settings import URL_TEMPLATE


def get_urls_generator(lag: int = 5):
    current_date = dt.datetime.utcnow()
    reference = current_date - dt.timedelta(days=lag)

    def recursive_closure():
        for i in range(lag):
            yield URL_TEMPLATE.format(date=(reference + dt.timedelta(days=i)).strftime("%Y%m%d"))

    return recursive_closure


def get_text(lag: int = 5) -> Optional[str]:
    urls_generator = get_urls_generator(lag=lag)
    for url in urls_generator():
        response = requests.get(url)
        if not response.ok:
            continue
        return response.text
