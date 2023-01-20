import json
import time

import requests
from scrapper import scrapper
import schedule

import logging
logging.basicConfig(filename='main.log', filemode='w', format='[%(levelname)s] %(asctime)s | %(name)s.%(funcName)s - %(message)s')

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
        def schedule_job():
            schedule.every().hour.do(scrapper, send_webhook)
            return schedule.CancelJob

        schedule.every().day.at('09:00').do(schedule_job)

        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as error:
        logging.critical(f"ERROR: {error}")
