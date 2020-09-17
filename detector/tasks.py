import logging
from datetime import timedelta, datetime, time
from app.celery import app
from celery.decorators import periodic_task
from celery.schedules import crontab
from detector.models import ActionSettings, BearDetect
from .const import HISTORICAL_DATA
from .parser import parse_data, fetch_current_price
from .fetcher import get_data
from .api_fbchat import send_message


@periodic_task(run_every=crontab(hour=15, minute=31))
def task_us_get_data():
    if HISTORICAL_DATA:
        for item in ActionSettings.objects.filter(enable=True):
            get_data(item)
    else:
        time = datetime.now().time()
        for item in ActionSettings.objects.filter(enable=True, time_from__lte=time, time_to__gte=time):
            BearDetect.objects.filter(
                symbol=item.symbol, time_resolution=item.time_resolution
            ).delete()
            get_data(item)


@periodic_task(run_every=timedelta(seconds=60))
def task_parse_data():
    if HISTORICAL_DATA:
        for item in ActionSettings.objects.filter(enable=True):
            parse_data(item)
    else:
        time = datetime.now().time()
        for item in ActionSettings.objects.filter(enable=True, time_from__lte=time, time_to__gte=time):
            parse_data(item)


@app.task
def task_force_get_data(item_id):
    logging.info('task_force_get_data {}'.format(item_id))
    item = ActionSettings.objects.get(id=item_id)
    logging.info('item {}'.format(item))
    if item:
        get_data(item)


@app.task
def task_triger_move(bear_id, item_id):
    logging.info('task_triger_move {} {}'.format(bear_id, item_id))
    item = ActionSettings.objects.get(id=item_id)
    bear = BearDetect.objects.get(id=bear_id)
    if item and bear:
        current_price = fetch_current_price(item)
        send_message(bear, item, current_price)

