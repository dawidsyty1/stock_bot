import json
import logging
import requests
from datetime import datetime, timedelta
from .const import BASE_URL_CANDLE, BASE_URL_QUOTE, HISTORICAL_DATA


class REQUEST_PARAMETERS:
    SYMBOL = 'symbol'
    TOKEN = 'token'
    FROM = 'from'
    TO = 'to'
    RESOLUTION = 'resolution'


def get_last_5_minutes_data(symbol, token, resolution):
    from_date = (datetime.now() + timedelta(minutes=-int(resolution) * 2)).strftime('%s')
    if HISTORICAL_DATA:
        from_date = (datetime.now() + timedelta(days=-1, minutes=0)).strftime('%s')

    response = requests.get(
        BASE_URL_CANDLE,
        {
            REQUEST_PARAMETERS.SYMBOL: symbol,
            REQUEST_PARAMETERS.RESOLUTION: resolution,
            REQUEST_PARAMETERS.FROM: from_date,
            REQUEST_PARAMETERS.TO: datetime.now().replace(second=1).strftime('%s'),
            REQUEST_PARAMETERS.TOKEN: token,
        }
    )

    serialized_response = {}

    try:
        serialized_response = response.json()
    except json.decoder.JSONDecodeError:
        logging.info('Exception JSONG: {}'.format(response.content))
    return serialized_response


def get_last_30_days_data(symbol, resolution, token):
    to_date = (datetime.now() + timedelta(days=-1)).replace(second=0, hour=0, minute=1).strftime('%s')
    if HISTORICAL_DATA:
        to_date = (datetime.now() + timedelta(days=-2)).replace(second=0, hour=0, minute=1).strftime('%s')

    response = requests.get(
        BASE_URL_CANDLE,
        {
            REQUEST_PARAMETERS.SYMBOL: symbol,
            REQUEST_PARAMETERS.RESOLUTION: resolution,
            REQUEST_PARAMETERS.FROM: (
                    datetime.now() + timedelta(days=-30)
            ).replace(second=0, hour=0, minute=1).strftime('%s'),
            REQUEST_PARAMETERS.TO: to_date,
            REQUEST_PARAMETERS.TOKEN: token,
        }
    )

    try:
        serialized_response = response.json()
    except json.decoder.JSONDecodeError:
        logging.info('Exception JSONG: {}'.format(response.content))

    return serialized_response


def get_last_data(symbol, token):
    serialized_response = {}
    response = requests.get(
        BASE_URL_QUOTE,
        {
            REQUEST_PARAMETERS.SYMBOL: symbol,
            REQUEST_PARAMETERS.TOKEN: token,
        }
    )

    try:
        serialized_response = response.json()
    except json.decoder.JSONDecodeError:
        logging.info('Exception JSONG: {}'.format(response.content))
    return serialized_response
