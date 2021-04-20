import json
import pandas as pd
from bot_manager.helper import setup_dir, indicators
# from fetcher.finnhub import (
#     get_historical_idicator_data,
#     get_last_two_interval_data_with_indicator,
#     get_data_for_backtest
# )


def grab_data(item):
    setup_dir(item.name)

    # for indicator in indicators(item):
    #     serialized_response = get_last_two_interval_data_with_indicator(item, indicator)
    #     df = pd.DataFrame.from_dict(serialized_response)
    #     df.insert(0, "datetime", pd.to_datetime(df.t, unit='s'), True)
    #     df.insert(0, "time", pd.to_datetime(df.t, unit='s').dt.time, True)
    #     df = df[(df.time >= item.time_from) & (df.time <= item.time_to)]
    #     df.to_csv(f'data/{item.name}/{indicator}.csv')


def grab_data_old(item):
    entries = [key for key in json.loads(item.strategy.entry_rule).keys()]
    exitst = [key for key in json.loads(item.strategy.exit_rule).keys()]

    setup_dir(item.name)

    for inticator in set(entries + exitst):
        # serialized_response = get_historical_idicator_data(item, inticator)
        serialized_response = {}
        keys_response = [key for key in serialized_response.keys()]
        data = serialized_response[keys_response[1]]
        lenght = 500 if len(data.items()) > 500 else len(data.items())
        data = dict(list(data.items())[:lenght])
        df = pd.DataFrame.from_dict(data)
        df.to_csv(f'data/{item.name}/{inticator}.csv')


def grab_data_backtest(item, days_back):
    setup_dir(f'backtest/{item.name}/{days_back}')

    for indicator in indicators(item):
        # serialized_response = get_data_for_backtest(item, indicator, days_back)
        serialized_response = {}
        df = pd.DataFrame.from_dict(serialized_response)
        df.insert(0, "datetime", pd.to_datetime(df.t, unit='s'), True)
        df.insert(1, "time", pd.to_datetime(df.t, unit='s').dt.time, True)
        df = df[(df.time >= item.time_from) & (df.time <= item.time_to)]
        df.to_csv(f'data/backtest/{item.name}/{days_back}/{indicator}.csv')
