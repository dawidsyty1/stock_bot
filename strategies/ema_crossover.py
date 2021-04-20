import talib
from utility.statistics import is_growing
from utility.ta_lib import ema
from fetchers.finnhub import fetch_dataframe


async def ema_crossover(ticker):
    timeperiod = 200

    stocks60 = fetch_dataframe(ticker, timeframe='60')
    stocks60 = ema(stocks60, timeperiod)

    if is_growing(stocks60.ema.to_numpy()):
        stocks = fetch_dataframe(ticker, timeframe='5')
        stocks = ema(stocks, timeperiod)
        stocks = ema(stocks, 20, name='ema_f')

        # if before_ema > before_ema_f and last_ema < last_ema_f:
        #     print('value')