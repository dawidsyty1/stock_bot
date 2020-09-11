import logging
import csv
from .helper import to_hours_dictionary, fast_average
from .api_finnhub import get_last_30_days_data


def get_data(symbol, token, resolution):
    serialized_response = get_last_30_days_data(symbol, resolution, token)

    if serialized_response == {}:
        logging.info('Error [{}] serialized response empty'.format(symbol))
        return

    try:
        hours_dictionary = to_hours_dictionary(serialized_response)
    except Exception as error:
        logging.info('Exception {}: Symbol: {}, error {}'.format(type(error), symbol, error))
        return

    hours_dictionary_average = {
        key: fast_average(value)
        for key, value in hours_dictionary.items()
    }

    if hours_dictionary_average == {}:
        logging.info('Error [{}] hours dictionary average empty'.format(symbol))
        return

    with open(f'data/{symbol}_average.csv', 'w') as file:
        spamwriter = csv.writer(file, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for index, (key, value) in enumerate(hours_dictionary_average.items()):
            spamwriter.writerow([index, key, value])
