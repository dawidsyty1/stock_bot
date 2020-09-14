from fbchat import Client
from fbchat.models import *

USER = '+48723893528'
PASSOWRD = 'bot12345'

client = Client(USER, PASSOWRD)


def send_message(bear):
    if not client.isLoggedIn():
        client.login(USER, PASSOWRD)

    client.send(
        Message(text='{}: {} volume: {} max_volume: {}'.format(bear.bear, bear.symbol, bear.volume, bear.max_volume)),
        thread_id='100000518793275', thread_type=ThreadType.USER)
    client.logout()
