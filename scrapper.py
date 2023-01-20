from datetime import datetime
import requests
from bs4 import BeautifulSoup

import logging
logging.basicConfig(filename='scrapper.log', filemode='w', format='[%(levelname)s] %(asctime)s | %(name)s.%(funcName)s - %(message)s')

BASE_URL = "https://csitgeu.in/wp/"


def get_current_date():
    current_date = datetime.now().date()
    return {
        "year": str(current_date.year),
        "month": str(current_date.month) if current_date.month > 9 else "0"+str(current_date.month),
        "day": str(current_date.day) if current_date.day > 9 else "0"+str(current_date.day)
    }


def scrapper(callback):
    date = get_current_date()
    last_notice_datetime = datetime.now().astimezone()
    try:
        logging.info(f"Fetching notices dated: {date['year']}/{date['month']}/{date['day']}...")
        response = requests.get(f"{BASE_URL}{date['year']}/{date['month']}/{date['day']}")
        logging.info(f"Response received for notices dated: {date['year']}/{date['month']}/{date['day']}...")
        soup = BeautifulSoup(response.content, 'html.parser')
        if response.status_code == 200:
            notices = soup.findAll('article')
            logging.info(f"Fetched {len(notices)} notice(s)")
            for notice in notices:
                timestamp = notice.find_next('span', class_='entry-date').find('time').get('datetime')
                notice_datetime = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S%z')
                logging.info(f"Last recent notice timestamp: {last_notice_datetime}")
                logging.info(f"Current notice timestamp: {notice_datetime}")
                if notice_datetime > last_notice_datetime:
                    last_notice_datetime = notice_datetime
                    title = notice.find_next('h1', class_='entry-title').text
                    url = notice.find_next('h1', class_='entry-title').find('a').get('href')
                    logging.info("Calling send_webhook callback...")
                    callback({
                        "content": None,
                        "embeds": [
                            {
                                "title": title,
                                "url": url,
                                "color": 1756421,
                                "author": {
                                    "name": "NEW NOTICE!"
                                },
                                "timestamp": notice_datetime.strftime('%Y-%m-%dT%H:%M:%S')+'Z'
                            }
                        ],
                        "attachments": []
                    })
        else:
            logging.warning("Unable to fetch notices. Reason: no notices for given date or incorrect request.")
    except Exception as error:
        logging.exception(f"ERROR: {error}")
