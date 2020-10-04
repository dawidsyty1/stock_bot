import requests
import logging

TO = '723893528'
TOKEN = 'cb6904bc-0ac5-4354-812e-b7fb0c2c80a9'
BASE_URL = 'https://api2.smsplanet.pl/sms'
PASSOWRD = 'Bot12345!'


def send_sms(bear):
    logging.info(f'{bear.name} price: {bear.price_percenage} volume: {bear.volume_percenage}')
    response = requests.post(BASE_URL, {
        'key': TOKEN,
        'from': 'Bot',
        'password': PASSOWRD,
        'to': TO,
        'msg': f'{bear.name} price: {bear.price_percenage} volume: {bear.volume_percenage}'
    })
    logging.info(f'Send sms: {response.text}')
