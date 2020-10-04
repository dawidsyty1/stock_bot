import logging
import csv
from datetime import datetime
from .helper import percenage, get_hours_dictionary_average
from .api_finnhub import get_last_5_minutes_data, get_last_data
from .models import BearDetect, TimeResolutions
from .const import TIME_FORMAT, HISTORICAL_DATA


def parse_response_data(serialized_response, hours_dictionary_average, item):
    logging.info('serialized_response {}'.format(serialized_response))
    for index, timestamp in enumerate(serialized_response['t']):
        try:
            time_key = datetime.fromtimestamp(timestamp).strftime(TIME_FORMAT)
            fast_average_value_test = get_hours_dictionary_average(hours_dictionary_average, time_key)
            volume = serialized_response['v'][index]
            divide_by = TimeResolutions().time_divide(item.time_resolution)
            fast_average_value = float(fast_average_value_test)/divide_by
            volumen_changed_percentage = ((int(volume) / int(fast_average_value)) * 100)
            price_changed_percentage = (float(serialized_response['o'][index]) / float(serialized_response['c'][index]))

            logging.info(
                'Symbol: {} time: {}, volume: {} fast_average_value: {} volumen_changed_percentage: {}\n , open: {}, close {} changed price {} o > c {} out {}'.format(
                    item.symbol,
                    time_key,
                    volume,
                    int(fast_average_value),
                    volumen_changed_percentage,
                    serialized_response['o'][index],
                    serialized_response['c'][index],
                    (float(serialized_response['o'][index]) / float(serialized_response['c'][index])) / 100,
                    serialized_response['o'][index] > serialized_response['c'][index],
                    volumen_changed_percentage > item.volume_percenage,
                )
            )
            if volumen_changed_percentage > item.volume_percenage:
                bear = BearDetect.objects.filter(
                    time=time_key, symbol=item.symbol, time_resolution=item.time_resolution
                )

                if len(bear) == 0:
                    from .tasks import task_triger_move
                    bear = BearDetect(
                        time=time_key,
                        symbol=item.symbol,
                        name=item.name,
                        price_percenage=price_changed_percentage,
                        volume_percenage=volumen_changed_percentage,
                        action_settings=item,
                        volume=str(volume),
                        max_volume=str(fast_average_value),
                        time_resolution=item.time_resolution,
                        price_open=serialized_response['o'][index],
                        price_close=serialized_response['c'][index],
                    )
                    bear.save()
                    if item.send_sms:
                        task_triger_move.delay(bear.id)

        except Exception as error:
            logging.info('Error {} {} {}'.format(error, type(error), item.symbol))


def parse_data(item):
    try:
        reader = csv.reader(open(f'data/{item.symbol}_15_average.csv'))
    except FileNotFoundError:
        from .tasks import task_force_get_data
        logging.info('Error [{}] hours dictionary average empty'.format(item.symbol))
        task_force_get_data.delay(item.id)
        return

    hours_dictionary_average = {
        row[0].split(' ')[1]: row[0].split(' ')[2]
        for row in reader
    }

    if hours_dictionary_average == {}:
        from .tasks import task_force_get_data
        logging.info('Error [{}] hours dictionary average empty'.format(item.symbol))
        task_force_get_data.delay(item.id)
        return

    serialized_response = get_last_5_minutes_data(item)

    if serialized_response == {}:
        logging.info('Error [{}] serialized response empty'.format(item.symbol))
        return

    try:
        parse_response_data(
            serialized_response, hours_dictionary_average, item
        )
    except Exception as error:
        logging.info('Exception {}: error {} symbol: {},'.format(type(error), error, item.symbol))


def fetch_current_price(item):
    if HISTORICAL_DATA:
        return None

    serialized_response = get_last_data(item)

    if serialized_response == {}:
        return None

    return serialized_response['c']
