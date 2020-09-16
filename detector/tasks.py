import logging
from datetime import timedelta, datetime, time
from app.celery import app
from celery.decorators import periodic_task
from celery.schedules import crontab
from detector.models import ActionSettings, BearDetect
from .const import HISTORICAL_DATA
from .parser import parse_data, triger_fb_message
from .fetcher import get_data
from .api_fbchat import send_message


@periodic_task(run_every=crontab(hour=15, minute=31))
def task_us_get_data():
    if HISTORICAL_DATA:
        for item in ActionSettings.objects.filter(enable=True):
            get_data(item.symbol, item.token, item.time_resolution)
    else:
        time = datetime.now().time()
        for item in ActionSettings.objects.filter(enable=True, time_from__lte=time, time_to__gte=time):
            BearDetect.objects.filter(
                symbol=item.symbol, time_resolution=item.time_resolution
            ).delete()
            get_data(item.symbol, item.token, item.time_resolution)


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
def task_force_get_data(symbol, token, time_resolution):
    get_data(symbol, token, time_resolution)


@app.task
def task_triger_move(symbol, close_price, token, volume, max_volume, time, bull_market):
    logging.info('task_triger_move for {}, close_price {} volume {}, max_volume {}'.format(symbol, close_price, volume, max_volume))
    if triger_fb_message(symbol, close_price, token, bull_market):
        send_message(time, symbol, volume, max_volume, bull_market)

