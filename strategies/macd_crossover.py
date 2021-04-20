from utility.statistics import is_growing
from utility.ta_lib import ema, macd
from fetchers.finnhub import fetch_dataframe


def is_bellow_zero(stocks):
    if stocks.macd.to_numpy()[-1] < 0 and stocks.macdsignal.to_numpy()[-1] < 0:
        return True
    return False


def is_cross(stocks):
    if stocks.macd.to_numpy()[-1] > stocks.macdsignal.to_numpy()[-1]:
        return True
    return False


async def macd_crossover(ticker):
    timeperiod = 200
    stocks60 = fetch_dataframe(ticker, timeframe='60')
    stocks60 = ema(stocks60, timeperiod)

    if is_growing(stocks60.ema.to_numpy()):
        stocks = fetch_dataframe(ticker, timeframe='5')
        stocks = macd(stocks)
        if is_bellow_zero(stocks) and is_cross(stocks):
            print('macd crossover')

