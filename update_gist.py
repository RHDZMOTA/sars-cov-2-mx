import json
import logging
from typing import Dict, Tuple

#from apscheduler.schedulers.blocking import BlockingScheduler
import requests

from sars_cov_2_mx.utils import get_text
from sars_cov_2_mx.settings import (
    get_logger,
    COV_FILENAME,
    COV_GIST_ID,
    COV_TOKEN,
)


#sched = BlockingScheduler()
logger = get_logger(name=__name__)


def get_headers() -> Dict[str, str]:
    return {
        "Authorization": f"token {COV_TOKEN}"
    }


def get_payload() -> Tuple[str, Dict]:
    response = get_text(lag=3)
    if not response:
        raise ValueError("Error when downloading the latest data.")

    date, latest_data = response
    return date, {
            "files": {
                COV_FILENAME: {
                    "content": latest_data
                }
            }
        }


#@sched.scheduled_job('cron', day_of_week='mon-sun', hour=17)
def main():
    headers = get_headers()
    date, payload = get_payload()
    gist_url = f"https://api.github.com/gists/{COV_GIST_ID}"

    logger.info("Attempting Gist Update with data from: %s", date)
    response = requests.patch(
        gist_url,
        data=json.dumps(payload),
        headers=headers,
    )
    if not response.ok:
        logger.error(response.text)
        raise ValueError("Response not okay.")
    logger.info("Ok!")


if __name__ == "__main__":
    #sched.start()
    main()

