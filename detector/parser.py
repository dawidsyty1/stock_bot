import logging
import csv
from datetime import datetime
from .helper import percenage, get_hours_dictionary_average
from .api_finnhub import get_last_5_minutes_data, get_last_data
from .models import BearDetect
from .const import TIME_FORMAT, HISTORICAL_DATA


def parse_response_data(serialized_response, hours_dictionary_average, item):
    logging.info('serialized_response {}'.format(serialized_response))
    for index, timestamp in enumerate(serialized_response['t']):
        try:
            time_key = datetime.fromtimestamp(timestamp).strftime(TIME_FORMAT)
            fast_average_value = get_hours_dictionary_average(hours_dictionary_average, time_key)
            volume = serialized_response['v'][index]
            max_volume = percenage(float(fast_average_value), item.volume_percenage)
            logging.info(
                'Symbol: {} time: {}, volume: {} max_volume: {} changed volume: {}, open: {}, close {} changed price {} o > c {} out {}'.format(
                    item.symbol,
                    time_key,
                    volume,
                    int(max_volume),
                    (float(max_volume) / float(volume)) / 100,
                    serialized_response['o'][index],
                    serialized_response['c'][index],
                    (float(serialized_response['o'][index]) / float(serialized_response['c'][index])) / 100,
                    serialized_response['o'][index] > serialized_response['c'][index],
                    volume > max_volume,
                )
            )
            if volume > max_volume:
                if item.bull and serialized_response['o'][index] < serialized_response['c'][index] or\
                        not item.bull and serialized_response['o'][index] > serialized_response['c'][index]:
                    bear = BearDetect.objects.filter(
                        time=time_key, symbol=item.symbol, time_resolution=item.time_resolution
                    )

                    if len(bear) == 0:
                        from .tasks import task_triger_move
                        bear = BearDetect(
                            time=time_key,
                            symbol=item.symbol,
                            volume=str(volume),
                            max_volume=str(max_volume),
                            time_resolution=item.time_resolution,
                            price_open=serialized_response['o'][index],
                            price_close=serialized_response['c'][index],
                        )
                        bear.save()
                        task_triger_move.delay(
                            item.symbol, serialized_response['c'][index], item.token, volume, max_volume, time_key
                        )

        except Exception as error:
            logging.info('Error {} {} {}'.format(error, type(error), item.symbol))


def parse_data(item):
    try:
        reader = csv.reader(open(f'data/{item.symbol}_{item.time_resolution}_average.csv'))
    except FileNotFoundError:
        from .tasks import task_force_get_data
        logging.info('Error [{}] hours dictionary average empty'.format(item.symbol))
        task_force_get_data.delay(item.symbol, item.token, item.time_resolution)
        return

    hours_dictionary_average = {
        row[0].split(' ')[1]: row[0].split(' ')[2]
        for row in reader
    }

    if hours_dictionary_average == {}:
        logging.info('Error [{}] hours dictionary average empty'.format(item.symbol))
        return

    serialized_response = get_last_5_minutes_data(item.symbol, item.token, item.time_resolution)

    if serialized_response == {}:
        logging.info('Error [{}] serialized response empty'.format(item.symbol))
        return

    try:
        parse_response_data(
            serialized_response, hours_dictionary_average, item
        )
    except Exception as error:
        logging.info('Exception {}: error {} symbol: {},'.format(type(error), error, item.symbol))


def triger_fb_message(symbol, close_price, token):
    if HISTORICAL_DATA:
        return True

    serialized_response = get_last_data(symbol, token)
    if close_price > serialized_response['c']:
        return True
    return False
