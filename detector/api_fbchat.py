from fbchat import Client
import logging
from fbchat.models import *

USER = '+48723893528'
PASSOWRD = 'Bot12345!'


def send_message(bear, item, current_price):
    try:
        client = Client(USER, PASSOWRD)
        if not client.isLoggedIn():
            client.login(USER, PASSOWRD)
        current_price = current_price if current_price is not None else ''

        client.send(
            Message(text='{}: {} volume: {} max_volume: {} bull_market: {} current_price: {}'.format(
                bear.time, item.symbol, bear.volume, bear.max_volume, item.bull_market, current_price
            )),
            thread_id='100000518793275', thread_type=ThreadType.USER)
        client.logout()
    except Exception as error:
        logging.info('Send message error: {}'.format(error))
