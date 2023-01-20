from datetime import datetime
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://csitgeu.in/wp/"


def get_current_date():
    current_date = datetime.now().date()
    return {
        "year": str(current_date.year),
        "month": str(current_date.month) if current_date.month > 9 else "0"+str(current_date.month),
        "day": str(current_date.day) if current_date.day > 9 else "0"+str(current_date.day)
    }


def scrapper():
    date = get_current_date()
    last_notice_datetime = datetime.now().astimezone()
    try:
        response = requests.get(f"{BASE_URL}{date['year']}/{date['month']}/{date['day']}")
        soup = BeautifulSoup(response.content, 'html.parser')
        if response.status_code == 200:
            notices = soup.findAll('article')
            for notice in notices:
                timestamp = notice.find_next('span', class_='entry-date').find('time').get('datetime')
                notice_datetime = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S%z')
                if notice_datetime > last_notice_datetime:
                    last_notice_datetime = notice_datetime
                    title = notice.find_next('h1', class_='entry-title').text
                    url = notice.find_next('h1', class_='entry-title').find('a').get('href')
                    # TODO => send message
                    print("NEW NOTICE:", title)
                    print(url)
                    print(notice_datetime)
        else:
            pass
    except Exception as error:
        print(error)
