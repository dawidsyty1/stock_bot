import json
import pandas as pd
from datetime import datetime
from bot_manager.helper import indicators
import logging
from bot_manager.models import Trade
import numpy as np


def parse_entry(key, entry, df):
    df = df[df[key] > 0]
    if '<' in entry:
        value = float(entry.replace('<', ''))
        df = df[df[key] < value]
    elif '>' in entry:
        value = float(entry.replace('>', ''))
        df = df[df[key] > value]

    return df


def valid_rules(item):
    entry_rules = json.loads(item.strategy.entry_rule)
    data_indicator = {}
    for indicator in indicators(item):
        df = pd.read_csv(f'data/{item.name}/{indicator}.csv')
        for key, entry in entry_rules[indicator].items():
            df = parse_entry(key, entry, df)
        data_indicator[indicator] = df['datetime'].to_numpy()
    return data_indicator


def compare_results(item, data_indicator):
    final_array = []
    for indicator in indicators(item):
        if len(data_indicator[indicator]) == 0:
            logging.info('compare_results not found')
            return []
        if len(final_array) == 0:
            final_array = data_indicator[indicator]
        else:
            final_array = np.intersect1d(final_array, data_indicator[indicator])

    return final_array


def start_trade(item, result_array):
    datetime_entry_rule = datetime.fromisoformat(result_array[-1])
    trade, created = Trade.objects.get_or_create(datetime_entry_rule=datetime_entry_rule, bot_setting=item)
    if created:
        trade.price_open = '123'
        trade.datetime_entry = datetime.now()
        trade.save()


def parse_item(item):
    data_indicator = valid_rules(item)
    result_array = compare_results(item, data_indicator)
    if len(result_array) != 0:
        start_trade(item)


def parse_trade(item):
    print('parse_trade', item)


def valid_rules_backtest(item, days_back):
    entry_rules = json.loads(item.strategy.entry_rule)
    data_indicator = {}
    for indicator in indicators(item):
        df = pd.read_csv(f'data/backtest/{item.name}/{days_back}/{indicator}.csv')
        for key, entry in entry_rules[indicator].items():
            df = parse_entry(key, entry, df)
        data_indicator[indicator] = df['datetime'].to_numpy()
    return data_indicator


def start_trade_backtest(item, result_array):
    datetime_entry_rule = datetime.fromisoformat(result_array[-1])
    trade, created = Trade.objects.get_or_create(datetime_entry_rule=datetime_entry_rule, bot_setting=item)
    if created:
        trade.price_open = '123'
        trade.datetime_entry = datetime_entry_rule
        trade.save()


def parse_backtest_data(item, days_back):
    data_indicator = valid_rules_backtest(item, days_back)
    print(data_indicator)
    result_array = compare_results(item, data_indicator)
    if len(result_array) != 0:
        start_trade_backtest(item, result_array)

