import talib
import numpy as np
from scipy.signal import argrelextrema
from utility.statistics import is_growing
from utility.ta_lib import ema, rsi
from fetchers.finnhub import fetch_dataframe


def is_bearish_divergence(dataframe):
    try:
        rsi_data = dataframe.rsi.to_numpy()
        close_data = dataframe.c.to_numpy()
        values_price = [close_data[value] for value in argrelextrema(close_data, np.less)[0]]
        values_rsi = [rsi_data[value] for value in argrelextrema(rsi_data, np.less)[0]]

        if len(values_rsi) > 7 and min(values_rsi) < 35:
            rsi_minimums = np.array(values_rsi, dtype='f8')
            if len(rsi_minimums) > 7:
                rsi_minimums = talib.SMA(rsi_minimums, int(len(rsi_minimums) - 5))
                rsi_minimums = rsi_minimums[~np.isnan(rsi_minimums)]

            price = np.array(values_price, dtype='f8')
            if len(price) > 10:
                price = talib.SMA(price, int(len(price) - 5))
                price = price[~np.isnan(price)]

            if np.all(np.diff(rsi_minimums) > 0) and np.all(np.diff(price) < 0):
                return True
    except IndexError as error:
        pass

    return False


async def rsi_bearish(ticker):
    timeperiod = 200

    stocks60 = fetch_dataframe(ticker, timeframe='60')
    stocks60 = ema(stocks60, timeperiod)

    if is_growing(stocks60.ema.to_numpy()):
        stocks = fetch_dataframe(ticker, timeframe='5')
        stocks = rsi(stocks, timeperiod)
        if is_bearish_divergence(stocks):
            print('test')
