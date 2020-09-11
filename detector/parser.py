import logging
import csv
from datetime import datetime
from .helper import percenage, get_hours_dictionary_average
from .api_finnhub import get_last_5_minutes_data
from .models import BearDetect
from .const import TIME_FORMAT


def parse_response_data(serialized_response, hours_dictionary_average, symbol, percenage_value):
    logging.info('serialized_response {}'.format(serialized_response))
    for index, timestamp in enumerate(serialized_response['t']):
        try:
            time_key = datetime.fromtimestamp(timestamp).strftime(TIME_FORMAT)
            fast_average_value = get_hours_dictionary_average(hours_dictionary_average, time_key)
            volume = serialized_response['v'][index]
            max_volume = percenage(float(fast_average_value), percenage_value)
            if volume > max_volume and serialized_response['o'][index] > serialized_response['c'][index]:
                bear = BearDetect()
                bear.symbol = symbol
                bear.time = time_key
                bear.volume = str(volume)
                bear.max_volume = str(max_volume)
                bear.price_open = serialized_response['o'][index]
                bear.price_close = serialized_response['c'][index]
                bear.save()

            logging.info(
                'Symbol: {} time: {}, volume: {} max_volume: {} changed volume: {}, open: {}, close {} changed price {} o > c {} out {}'.format(
                    symbol,
                    time_key,
                    volume,
                    int(max_volume),
                    (float(max_volume) / float(volume)) / 100,
                    serialized_response['o'][index],
                    serialized_response['c'][index],
                    (float(serialized_response['o'][index])/float(serialized_response['c'][index]))/100,
                    serialized_response['o'][index] > serialized_response['c'][index],
                    volume > max_volume,
                )
            )
        except Exception as error:
            logging.info('Error {} {} {}'.format(error, type(error), symbol))


def parse_data(symbol, token, resolution, volume_percenage):
    reader = csv.reader(open(f'data/{symbol}_average.csv'))

    hours_dictionary_average = {
        row[0].split(' ')[1]: row[0].split(' ')[2]
        for row in reader
    }

    if hours_dictionary_average == {}:
        logging.info('Error [{}] hours dictionary average empty'.format(symbol))
        return

    serialized_response = get_last_5_minutes_data(symbol, token, resolution)

    if serialized_response == {}:
        logging.info('Error [{}] serialized response empty'.format(symbol))
        return

    try:
        parse_response_data(serialized_response, hours_dictionary_average, symbol, volume_percenage)
    except Exception as error:
        logging.info('Exception {}: error {} symbol: {},'.format(type(error), error, symbol))

