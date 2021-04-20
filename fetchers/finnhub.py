import pandas as pd
import talib
import datetime
import requests

BASE_URL = 'https://finnhub.io/api/v1/stock/candle'
TOKEN_VALUE = 'btdnr4v48v6p1d4q5ot0'


class REQUEST_PARAMETERS:
    SYMBOL = 'symbol'
    TOKEN = 'token'
    FROM = 'from'
    TO = 'to'
    RESOLUTION = 'resolution'


def fetch_dataframe(
        ticker, timeframe='1',
):
    data_to = datetime.datetime.now()
    data_from = data_to - datetime.timedelta(days=30)

    response = requests.get(
        BASE_URL,
        {
            REQUEST_PARAMETERS.SYMBOL: ticker,
            REQUEST_PARAMETERS.RESOLUTION: timeframe,
            REQUEST_PARAMETERS.FROM: data_from.strftime('%s'),
            REQUEST_PARAMETERS.TO: data_to.strftime('%s'),
            REQUEST_PARAMETERS.TOKEN: TOKEN_VALUE
        }
    )

    serialized_response = response.json()
    dataframe = pd.DataFrame.from_dict(serialized_response)
    dataframe.insert(0, "datetime", pd.to_datetime(dataframe.t, unit='s'), True)
    return dataframe
