import requests
import feedparser
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime
import schedule
import time

flag = 0

def get_it_news():
    rss_url = "https://www.zdnet.com/news/rss.xml"
    feed = feedparser.parse(rss_url)

    news_list = []
    for entry in feed.entries:
        headline = entry.title
        link = entry.link
        news_list.append({"headline": headline, "link": link})

    return news_list


def send_slack_message(news, slack_token, channel):
    client = WebClient(token=slack_token)

    # 이모지 추가
    date_string = datetime.today().strftime("%Y-%m-%d")
    date_text = f":red_circle: ({date_string}) :red_circle:"

    # 뉴스 제목과 링크 추가
    news_text = f'<{news["link"]}|{news["headline"]}>'



    try:
        #뉴스기사 전송
        response = client.chat_postMessage(
            channel=channel,
            text=date_text + '\n' + news_text
        )
    except SlackApiError as e:
        print(f"Error: {e}")

def job():
    news_list = get_it_news()
    for news in news_list:
        send_slack_message(news, "xoxb-5102656250227-5099880916901-9w8RPxdxLUujwxT8utqK6ca3", "rss_feed")

schedule.every().day.at("08:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)