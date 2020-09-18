import logging
import csv
from datetime import timedelta, datetime
from app.celery import app
from celery.decorators import periodic_task
from celery.schedules import crontab
from detector.models import ActionSettings, BearDetect, StockType
from .const import HISTORICAL_DATA, MAX_NUMBERS_PER_TOKEN
from .parser import parse_data, fetch_current_price
from .fetcher import get_data
from .api_fbchat import send_message
from .api_finnhub import list_stock_data, list_forex_data, list_crypto_data
from .helper import synchronize_time


@app.task
def task_triger_parse_data_for(item_id):
    item = ActionSettings.objects.get(id=item_id)
    if item:
        parse_data(item)

@app.task
def task_force_get_data(item_id):
    logging.info('task_force_get_data {}'.format(item_id))
    item = ActionSettings.objects.get(id=item_id)
    logging.info('item {}'.format(item))
    if item:
        get_data(item)


@app.task
def task_set_tokens_from_file():
    try:
        reader = csv.reader(open('config/data_config/finnhub_accounts.csv'))
    except FileNotFoundError:
        logging.info('task_set_tokens_from_file')

        return

    tokens = [row[0].split(':')[1] for row in reader]
    logging.info('tokens {}'.format(tokens))
    counter = 0
    row = 0
    for item in ActionSettings.objects.filter(enable=True):
        if counter > MAX_NUMBERS_PER_TOKEN:
            counter = 0
            row = row + 1
        item.token = tokens[row]
        counter = counter + 1
        item.save()


@app.task
def task_enable_from_file():
    try:
        reader = csv.reader(open('config/data_config/nasdaq_companies.csv'))
    except FileNotFoundError:
        logging.info('task_set_tokens_from_file'.format())

        return

    symbols = [row[0] for row in reader]
    for item in ActionSettings.objects.filter(symbol__in=symbols):
        item.enable = True
        item.save()


@app.task
def task_delete_all_action_list():
    ActionSettings.objects.all().delete()


@app.task
def task_delete_all_data():
    import glob, os, os.path
    filelist = glob.glob(os.path.join('data', "*.csv"))
    for f in filelist:
        os.remove(f)


@app.task
def task_triger_move(bear_id, item_id):
    logging.info('task_triger_move {} {}'.format(bear_id, item_id))
    item = ActionSettings.objects.get(id=item_id)
    bear = BearDetect.objects.get(id=bear_id)
    if item and bear:
        current_price = fetch_current_price(item)
        send_message(bear, item, current_price)


@periodic_task(run_every=crontab(hour=1, minute=00))
def task_us_get_data():
    if HISTORICAL_DATA:
        for item in ActionSettings.objects.filter(enable=True):
            get_data(item)
    else:
        for item in ActionSettings.objects.filter(enable=True):
            BearDetect.objects.filter(
                symbol=item.symbol, time_resolution=item.time_resolution
            ).delete()
            task_delete_all_data.delay()
            get_data(item)


@periodic_task(run_every=crontab(hour=1, minute=00))
def task_update_action_list():
    def validator_description(description, symbol):
        return description if description != '' else symbol

    time_from = datetime.now().replace(second=0, hour=15, minute=30).time()
    time_to = datetime.now().replace(second=0, hour=22, minute=00).time()

    for item in list_stock_data():
        object, created = ActionSettings.objects.get_or_create(symbol=item['symbol'])
        object.name = validator_description(item['description'], item['symbol'])
        object.stock_type = StockType.STOCK
        object.time_from = time_from
        object.time_to = time_to
        object.save()

    time_from = datetime.now().replace(second=0, hour=1, minute=00).time()
    time_to = datetime.now().replace(second=0, hour=23, minute=00).time()

    for item in list_forex_data():
        object, created = ActionSettings.objects.get_or_create(symbol=item['symbol'])
        object.name = validator_description(item['description'], item['symbol'])
        object.stock_type = StockType.FOREX
        object.time_from = time_from
        object.time_to = time_to
        object.save()

    for item in list_crypto_data():
        object, created = ActionSettings.objects.get_or_create(symbol=item['symbol'])
        object.name = validator_description(item['description'], item['symbol'])
        object.stock_type = StockType.CRYPTO
        object.time_from = time_from
        object.time_to = time_to
        object.save()


@periodic_task(run_every=timedelta(seconds=60))
def task_parse_data():
    synchronize_time()
    if HISTORICAL_DATA:
        for item in ActionSettings.objects.filter(enable=True):
            parse_data(item)
    else:
        time = datetime.now().time()
        for item in ActionSettings.objects.filter(enable=True, time_from__lte=time, time_to__gte=time):
            task_triger_parse_data_for.delay(item.id)
