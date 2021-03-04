import json
import logging
import requests

ALPHA_VANTAGE = 'https://www.alphavantage.co/query?',

class REQUEST_PARAMETERS:
    SYMBOL = 'symbol'
    EXCHANGE = 'exchange'
    TOKEN = 'token'
    API_KEY = 'apikey'
    FROM = 'from'
    TO = 'to'
    RESOLUTION = 'resolution'
    INTERVAL = 'interval'
    FUNCTION = 'function'
    SERIES_TYPE = 'series_type'


def get_indicator_data(item, function):
    serialized_response = {}
    response = None
    if function == 'MACD':
        response = requests.get(
            ALPHA_VANTAGE,
            {
                REQUEST_PARAMETERS.FUNCTION: function,
                REQUEST_PARAMETERS.SYMBOL: item.symbol,
                REQUEST_PARAMETERS.INTERVAL: '30min',
                REQUEST_PARAMETERS.SERIES_TYPE: 'close',
                REQUEST_PARAMETERS.API_KEY: item.token,
            }
        )

    if function == 'STOCHF':
        response = requests.get(
            ALPHA_VANTAGE,
            {
                REQUEST_PARAMETERS.FUNCTION: function,
                REQUEST_PARAMETERS.SYMBOL: item.symbol,
                REQUEST_PARAMETERS.INTERVAL: '30min',
                REQUEST_PARAMETERS.API_KEY: item.token,
            }
        )


    try:
        serialized_response = response.json()
        logging.info('Exception JSON: {}'.format(response.request.url))
    except json.decoder.JSONDecodeError:
        logging.info('Exception JSON: {}'.format(response.request.url))
    return serialized_response