from fbchat import Client
from fbchat.models import *

USER = '+48723893528'
PASSOWRD = 'Bot12345!'


def send_message(time, symbol, volume, max_volume, bull_market):
    client = Client(USER, PASSOWRD)
    if not client.isLoggedIn():
        client.login(USER, PASSOWRD)

    client.send(
        Message(text='{}: {} volume: {} max_volume: {} bull_market: {}'.format(
            time, symbol, volume, max_volume, bull_market
        )),
        thread_id='100000518793275', thread_type=ThreadType.USER)
    client.logout()
