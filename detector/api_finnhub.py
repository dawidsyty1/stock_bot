import json
import logging
import requests
from datetime import datetime, timedelta
from .const import BASE_URL_CANDLE, BASE_URL_QUOTE, HISTORICAL_DATA, BASE_URL_FOREX_CANDLE, BASE_URL_CRYPTO_CANDLE
from .models import StockType


class REQUEST_PARAMETERS:
    SYMBOL = 'symbol'
    TOKEN = 'token'
    FROM = 'from'
    TO = 'to'
    RESOLUTION = 'resolution'


def candle_url(stock_type):
    base_url = ''
    if stock_type == StockType.STOCK:
        base_url = BASE_URL_CANDLE;
    elif stock_type == StockType.FOREX:
        base_url = BASE_URL_FOREX_CANDLE;
    elif stock_type == StockType.CRYPTO:
        base_url = BASE_URL_CRYPTO_CANDLE;
    else:
        raise NotImplemented
    return base_url


def get_last_5_minutes_data(item):
    from_date = (datetime.now() + timedelta(minutes=-int(item.time_resolution) * 2)).strftime('%s')
    if HISTORICAL_DATA:
        from_date = (datetime.now() + timedelta(days=-1, minutes=0)).strftime('%s')

    base_url = candle_url(item.stock_type)

    response = requests.get(
        base_url,
        {
            REQUEST_PARAMETERS.SYMBOL: item.symbol,
            REQUEST_PARAMETERS.RESOLUTION: item.time_resolution,
            REQUEST_PARAMETERS.FROM: from_date,
            REQUEST_PARAMETERS.TO: datetime.now().replace(second=1).strftime('%s'),
            REQUEST_PARAMETERS.TOKEN: item.token,
        }
    )

    serialized_response = {}

    try:
        serialized_response = response.json()
    except json.decoder.JSONDecodeError:
        logging.info('Exception JSONG: {}'.format(response.request.url))
    return serialized_response


def get_last_30_days_data(item):
    to_date = (datetime.now() + timedelta(days=-1)).replace(second=0, hour=0, minute=1).strftime('%s')
    if HISTORICAL_DATA:
        to_date = (datetime.now() + timedelta(days=-2)).replace(second=0, hour=0, minute=1).strftime('%s')

    base_url = candle_url(item.stock_type)

    response = requests.get(
        base_url,
        {
            REQUEST_PARAMETERS.SYMBOL: item.symbol,
            REQUEST_PARAMETERS.RESOLUTION: item.time_resolution,
            REQUEST_PARAMETERS.FROM: (
                    datetime.now() + timedelta(days=-30)
            ).replace(second=0, hour=0, minute=1).strftime('%s'),
            REQUEST_PARAMETERS.TO: to_date,
            REQUEST_PARAMETERS.TOKEN: item.token,
        }
    )

    try:
        serialized_response = response.json()
    except json.decoder.JSONDecodeError:
        logging.info('Exception JSONG: {}'.format(response.content))

    return serialized_response


def get_last_data(item):
    serialized_response = {}
    if item.stock_type == StockType.STOCK:
        response = requests.get(
            BASE_URL_QUOTE,
            {
                REQUEST_PARAMETERS.SYMBOL: item.symbol,
                REQUEST_PARAMETERS.TOKEN: item.token,
            }
        )
    else:
        return serialized_response

    try:
        serialized_response = response.json()
    except json.decoder.JSONDecodeError:
        logging.info('Exception JSON: {}'.format(response.request.url))
    return serialized_response
