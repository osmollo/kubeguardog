import json
import requests

from common import TELEGRAM_URL
from log import logger


def send_telegram_message(token, chat_id, text) -> None:
    url = f"{TELEGRAM_URL}/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "MarkdownV2",
        "disable_web_page_preview": False,
        "disable_notification": False,
        "reply_to_message_id": None
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(url=url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        logger.debug(f"Telegram message sent to {chat_id}")
    else:
        logger.error(f"Error sending telegram message to {chat_id} [status code: {response.status_code}]. REASON: {response.json()['description']}")
        print(f"Telegram URL: {url}")
        print(f"Body: {json.dumps(payload)}")
