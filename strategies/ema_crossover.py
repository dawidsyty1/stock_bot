import pandas as pd
import talib
import datetime
import requests
from utility.statistics import percentage

BASE_URL = 'https://finnhub.io/api/v1/stock/candle'
TOKEN_VALUE = 'btdnr4v48v6p1d4q5ot0'


class REQUEST_PARAMETERS:
    SYMBOL = 'symbol'
    TOKEN = 'token'
    FROM = 'from'
    TO = 'to'
    RESOLUTION = 'resolution'


async def ema_crossover(ticker):
    response = requests.get(
        BASE_URL,
        {
            REQUEST_PARAMETERS.SYMBOL: ticker,
            REQUEST_PARAMETERS.RESOLUTION: '60',
            REQUEST_PARAMETERS.FROM: datetime.datetime(2021, 3, 1, 23, 0).strftime('%s'),
            REQUEST_PARAMETERS.TO: datetime.datetime.now().strftime('%s'),
            REQUEST_PARAMETERS.TOKEN:TOKEN_VALUE
        }
    )

    serialized_response = response.json()
    df = pd.DataFrame.from_dict(serialized_response)
    df.insert(0, "datetime", pd.to_datetime(df.t, unit='s'), True)
    df['ema'] = talib.EMA(df.c, timeperiod=200)

    df = df.dropna()
    df60 = df.reset_index()

    response = requests.get(
        BASE_URL,
        {
            REQUEST_PARAMETERS.SYMBOL: ticker,
            REQUEST_PARAMETERS.RESOLUTION: '5',
            REQUEST_PARAMETERS.FROM: datetime.datetime(2021, 4, 1, 23, 0).strftime('%s'),
            REQUEST_PARAMETERS.TO: datetime.datetime.now().strftime('%s'),
            REQUEST_PARAMETERS.TOKEN:TOKEN_VALUE
        }
    )
    serialized_response = response.json()
    df = pd.DataFrame.from_dict(serialized_response)
    df.insert(0, "datetime", pd.to_datetime(df.t, unit='s'), True)
    df['ema'] = talib.EMA(df.c, timeperiod=200)
    df['ema_f'] = talib.EMA(df.c, timeperiod=20)
    df = df.dropna()
    df5 = df.reset_index()
    array = df60.ema.to_numpy()
    print(percentage(array[0], array[-1]))
    if percentage(array[0], array[-1]) < 99.5:
        array = df5.ema.to_numpy()
        before_ema = array[-5]
        last_ema = array[-1]

        array = df5.ema_f.to_numpy()
        before_ema_f = array[-5]
        last_ema_f = array[-1]

        if before_ema > before_ema_f and last_ema < last_ema_f:
            print('value')