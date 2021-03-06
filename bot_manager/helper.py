import logging
from datetime import datetime, timedelta, time
import glob
import os
import json

BASE_URL = 'https://finnhub.io/api/v1/stock/candle'

TIME_RESOLUTION = 5
DELAY = 60
SHOW_WARRINGS = True
DURATION = True
DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:00'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:00'


class REQUEST_PARAMETERS:
    SYMBOL = 'symbol'
    TOKEN = 'token'
    FROM = 'from'
    TO = 'to'
    RESOLUTION = 'resolution'


def to_hours_dictionary(serialized_response, filter=True):

    time_key_array = [
        datetime.fromtimestamp(timestamp).strftime(TIME_FORMAT)
        for index, timestamp in enumerate(serialized_response['t'])
    ]

    time_key_array = sorted(time_key_array)

    hours_dictionary = {
        time_key: []
        for time_key in time_key_array
    }

    for index, timestamp in enumerate(serialized_response['t']):
        key_time = datetime.fromtimestamp(timestamp).strftime(TIME_FORMAT)
        hours_dictionary[key_time].append(serialized_response['v'][index])
    if filter:
        hours_dictionary = {
            key: value
            for key, value in hours_dictionary.items() if len(value) > 5
        }

    if len(hours_dictionary.keys()) == 0:
        raise Exception('hours_dictionary is empty')
    return hours_dictionary


def get_hours_dictionary_average(hours_dictionary, time_key):
    try:
        return hours_dictionary[time_key]
    except KeyError as error:
        time_key_pivot = datetime.strptime(time_key, TIME_FORMAT)
        result = min(
            list(hours_dictionary.keys())[index - 1]
            for index, item in enumerate(hours_dictionary.keys())
            if datetime.strptime(item, TIME_FORMAT) > time_key_pivot
        )
        logging.info('get_hours_dictionary_average {}'.format(result))
        return hours_dictionary[result]


def percenage(value, percenage_value):
    return value + (value * percenage_value / 100)


def fast_average(values):
    return sum(int(i) for i in values) / len(values)


def synchronize_time():
    import time
    logging.info('before {}'.format(datetime.now()))
    time.sleep(
        ((timedelta(minutes=1) + datetime.now()).replace(
            second=1) - datetime.now()).total_seconds()
    )
    logging.info('after {}'.format(datetime.now()))


def setup_dir(path):
    try:
        files = glob.glob(f'data/{path}/*')
        for f in files:
            os.remove(f)
    except FileNotFoundError:
        pass

    if not os.path.exists(f'data/{path}'):
        os.makedirs(f'data/{path}')


def indicators(item):
    entry_rules = json.loads(item.strategy.entry_rule)

    entries = [key for key in entry_rules.keys()]
    return set(entries)