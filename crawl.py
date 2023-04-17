import os
import requests
import feedparser
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime
import schedule
import time

# 0은 출력, 1은 미출력
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

def send_final_mention(slack_token, channel):
    client = WebClient(token=slack_token)

    try:
        response = client.chat_postMessage(
            channel=channel,
            text="<!channel>"
        )

    except SlackApiError as e:
        print(f"Error: {e}")

def job():
    global flag

    news_list = get_it_news()
    slack_token = os.environ["SLACK_TOKEN"]
    channel = "rss_feed"

    for news in news_list:
        send_slack_message(news, slack_token, channel)

    send_final_mention(slack_token, channel)

job()
#schedule.every().day.at("08:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
