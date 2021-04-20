import talib
import pandas as pd
from utility.statistics import percentage
from fetchers.finnhub import fetch_dataframe


async def ema_crossover(ticker):
    df = fetch_dataframe(ticker, timeframe=60)
    df['ema'] = talib.EMA(df.c, timeperiod=200)

    df = df.dropna()
    df60 = df.reset_index()

    df = fetch_dataframe(ticker, timeframe=60)
    df['ema'] = talib.EMA(df.c, timeperiod=200)
    df['ema_f'] = talib.EMA(df.c, timeperiod=20)
    df = df.dropna()
    df5 = df.reset_index()
    array = df60.ema.to_numpy()

    if percentage(array[0], array[-1]) < 99.5:
        array = df5.ema.to_numpy()
        before_ema = array[-5]
        last_ema = array[-1]

        array = df5.ema_f.to_numpy()
        before_ema_f = array[-5]
        last_ema_f = array[-1]

        if before_ema > before_ema_f and last_ema < last_ema_f:
            print('value')