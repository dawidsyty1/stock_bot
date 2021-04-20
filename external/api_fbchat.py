from fbchat import Client
import logging
from fbchat.models import *
import os


USER = os.environ.get("USER_FB", '')
PASSWORD = os.environ.get("PASSWORD_FB", '')


def send_message(bear, item, current_price):
    try:
        client = Client(USER, PASSWORD)
        if not client.isLoggedIn():
            client.login(USER, PASSWORD)
        current_price = current_price if current_price is not None else ''

        client.send(
            Message(text='{}: {} volume: {} max_volume: {} bull_market: {} current_price: {}'.format(
                bear.time, item.symbol, bear.volume, bear.max_volume, item.bull_market, current_price
            )),
            thread_id='100000518793275', thread_type=ThreadType.USER)
        # client.logout()
    except Exception as error:
        logging.info('Send message error: {}'.format(error))
