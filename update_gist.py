import json
from typing import Dict

from apscheduler.schedulers.blocking import BlockingScheduler
import requests

from sars_cov_2_mx.utils import get_text
from sars_cov_2_mx.settings import (
    COV_FILENAME,
    COV_GIST_ID,
    COV_TOKEN,
)


sched = BlockingScheduler()


def get_headers() -> Dict[str, str]:
    return {
        "Authorization": f"token {COV_TOKEN}"
    }


def get_payload() -> Dict:
    latest_data = get_text(lag=5)
    if not latest_data:
        raise ValueError("Error when downloading the latest data.")
    return {
            "files": {
                COV_FILENAME: {
                    "content": latest_data
                }
            }
        }


@sched.scheduled_job('cron', day_of_week='mon-sun', hour=17)
def main():
    headers = get_headers()
    payload = get_payload()
    response = requests.patch(
        f"https://api.github.com/gists/{COV_GIST_ID}",
        data=json.dumps(payload),
        headers=headers,
    )
    if not response.ok:
        raise ValueError("Error in main process: %s", response.text)


if __name__ == "__main__":
    sched.start()
