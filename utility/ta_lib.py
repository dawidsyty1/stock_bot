import talib


def ema(dataframe, period, name='ema'):
    dataframe[name] = talib.EMA(dataframe.c, timeperiod=period)
    dataframe = dataframe[period:]
    dataframe = dataframe.reset_index(drop=True)
    return dataframe


def rsi(dataframe, period, name='rsi'):
    dataframe[name] = talib.RSI(dataframe.c, timeperiod=period)
    dataframe = dataframe[period:]
    dataframe = dataframe.reset_index(drop=True)
    return dataframe


def macd(dataframe, fast=12, slow=35, signal=9):
    dataframe['macd'], dataframe['macdsignal'], dataframe['macdhist'] = talib.MACD(
        dataframe.c, fastperiod=fast, slowperiod=slow, signalperiod=signal
    )
    dataframe = dataframe.reset_index(drop=True)
    return dataframe
