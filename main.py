import time

import requests
from scrapper import scrapper
import schedule


WEBHOOK_URL = "https://discord.com/api/webhooks/1066061125709463633/uiPa_3GYsU95hJtjMoq3zBSRsd25hY4nidcpx_s89vsQBXXhjoJWZl3GX4S7Bx6hYC5k"


def send_webhook(data):
    try:
        response = requests.post(WEBHOOK_URL, data=data)
        if response.status_code == 200:
            pass
        else:
            pass
    except Exception as error:
        pass


if __name__ == '__main__':
    def schedule_job():
        schedule.every().hour.do(scrapper, send_webhook)
        return schedule.CancelJob

    schedule.every().day.at('09:00').do(schedule_job)

    while True:
        schedule.run_pending()
        time.sleep(1)
