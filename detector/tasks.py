import logging
from datetime import timedelta, datetime
from app.celery import app
from celery.decorators import periodic_task
from celery.schedules import crontab
from detector.models import ActionSettings, BearDetect, StockType
from .const import HISTORICAL_DATA
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
    for item in list_stock_data():
        object, created = ActionSettings.objects.get_or_create(symbol=item['symbol'])
        object.name = item['description']
        object.stock_type = StockType.STOCK
        object.save()

    for item in list_forex_data():
        object, created = ActionSettings.objects.get_or_create(symbol=item['symbol'])
        object.name = item['description']
        object.stock_type = StockType.FOREX
        object.save()

    for item in list_crypto_data():
        object, created = ActionSettings.objects.get_or_create(symbol=item['symbol'])
        object.name = item['description']
        object.stock_type = StockType.CRYPTO
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
