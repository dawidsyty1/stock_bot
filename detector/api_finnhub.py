import json
import logging
import requests
from datetime import datetime, timedelta
from .const import (
    BASE_URL_CANDLE,
    BASE_URL_QUOTE,
    HISTORICAL_DATA,
    BASE_URL_FOREX_CANDLE,
    BASE_URL_CRYPTO_CANDLE,
    TOKEN,
    DETECTOR_STOCK_SYMBOLS,
    DETECTOR_FOREX_SYMBOLS,
    DETECTOR_CRYPTO_SYMBOLS
)
from .models import StockType


class REQUEST_PARAMETERS:
    SYMBOL = 'symbol'
    EXCHANGE = 'exchange'
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
    logging.info('get_last_5_minutes_data {}'.format(response.request.url))
    serialized_response = {}

    try:
        serialized_response = response.json()
    except json.decoder.JSONDecodeError:
        logging.info('Exception JSONG: {}'.format(response.request.url))
    return serialized_response


def get_last_30_days_data(item):
    to_date = (datetime.now() + timedelta(days=-1)).replace(second=0, hour=1, minute=1).strftime('%s')
    if HISTORICAL_DATA:
        to_date = (datetime.now() + timedelta(days=-2)).replace(second=0, hour=0, minute=1).strftime('%s')

    base_url = candle_url(item.stock_type)
    days_from = 30

    response = requests.get(
        base_url,
        {
            REQUEST_PARAMETERS.SYMBOL: item.symbol,
            REQUEST_PARAMETERS.RESOLUTION: '15',
            REQUEST_PARAMETERS.FROM: (
                    datetime.now() + timedelta(days=-days_from)
            ).replace(hour=2, second=0, minute=1).strftime('%s'),
            REQUEST_PARAMETERS.TO: to_date,
            REQUEST_PARAMETERS.TOKEN: item.token,
        }
    )
    logging.info('get_last_30_days_data {}'.format(response.request.url))

    try:
        serialized_response = response.json()
    except json.decoder.JSONDecodeError:
        logging.info('Exception JSONG: {}'.format(response.request.url))

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


def list_stock_data(exchange='us'):
    response = requests.get(
        DETECTOR_STOCK_SYMBOLS,
        {
            REQUEST_PARAMETERS.EXCHANGE: exchange,
            REQUEST_PARAMETERS.TOKEN: TOKEN,
        }
    )
    try:
        return response.json()
    except json.decoder.JSONDecodeError:
        logging.info('list_stock_data: {}'.format(response.request.url))
    return []


def list_crypto_data(exchange='binance'):
    response = requests.get(
        DETECTOR_CRYPTO_SYMBOLS,
        {
            REQUEST_PARAMETERS.EXCHANGE: exchange,
            REQUEST_PARAMETERS.TOKEN: TOKEN,
        }
    )
    try:
        return response.json()
    except json.decoder.JSONDecodeError:
        logging.info('list_stock_data: {}'.format(response.request.url))
    return []


def list_forex_data(exchange='oanda'):
    response = requests.get(
        DETECTOR_FOREX_SYMBOLS,
        {
            REQUEST_PARAMETERS.EXCHANGE: exchange,
            REQUEST_PARAMETERS.TOKEN: TOKEN,
        }
    )
    try:
        return response.json()
    except json.decoder.JSONDecodeError:
        logging.info('list_forex_data: {}'.format(response.request.url))
    return []