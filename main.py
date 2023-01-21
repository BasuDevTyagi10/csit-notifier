import json
import time

import requests
from scrapper import scrapper
import schedule

import logging
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler(filename='logs.log')
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] %(asctime)s | %(name)s.%(funcName)s - %(message)s',
    handlers=[stream_handler, file_handler]
)

WEBHOOK_URL = "https://discord.com/api/webhooks/1066061125709463633/uiPa_3GYsU95hJtjMoq3zBSRsd25hY4nidcpx_s89vsQBXXhjoJWZl3GX4S7Bx6hYC5k"


def send_webhook(data):
    logging.info(f"Sending Webhook with title: {data.get('embeds', [{}])[0].get('title')}")
    try:
        response = requests.post(WEBHOOK_URL, headers={'Content-Type': 'application/json'}, data=json.dumps(data))
        if response.status_code == 200:
            logging.info(f"Webhook sent successfully with title: {data.get('embeds', [{}])[0].get('title')}")
        else:
            logging.error(f"Code [{response.status_code}]. Unable to send webhook: {response.content}")
    except Exception as error:
        logging.exception(f"ERROR: {error}")


if __name__ == '__main__':
    try:
        logging.info("Starting CSIT Notifier...")
        schedule.every().hour.do(scrapper, send_webhook)

        logging.info("Running scheduler: schedule.every().hour.do(scrapper, send_webhook)")
        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as error:
        logging.critical(f"ERROR: {error}")
