from fbchat import Client
from fbchat.models import *

USER = '+48723893528'
PASSOWRD = 'Bot12345!'


def send_message(time, symbol, volume, max_volume, bull_market, current_price):
    client = Client(USER, PASSOWRD)
    if not client.isLoggedIn():
        client.login(USER, PASSOWRD)
    current_price = current_price if current_price is not None else ''

    client.send(
        Message(text='{}: {} volume: {} max_volume: {} bull_market: {} current_price: {}'.format(
            time, symbol, volume, max_volume, bull_market, current_price
        )),
        thread_id='100000518793275', thread_type=ThreadType.USER)
    client.logout()
