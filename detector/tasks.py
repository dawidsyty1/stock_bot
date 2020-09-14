import logging
from datetime import timedelta, datetime, time
from app.celery import app
from celery.decorators import periodic_task
from celery.schedules import crontab
from detector.models import ActionSettings
from .parser import parse_data, triger_fb_message
from .fetcher import get_data
from .api_fbchat import send_message


@periodic_task(run_every=timedelta(seconds=600))
def task_us_get_data():
    time = datetime.now().time()
    for item in ActionSettings.objects.filter(enable=True, time_from__lte=time, time_to__gte=time):
        get_data(item.symbol, item.token, item.time_resolution)


@periodic_task(run_every=crontab(hour=15, minute=31))
def task_parse_data():
    time = datetime.now().time()
    for item in ActionSettings.objects.filter(enable=True, time_from__lte=time, time_to__gte=time):
        parse_data(item)


@app.task
def task_force_get_data(item):
    get_data(item.symbol, item.token, item.time_resolution)


@app.task
def task_triger_move(bear, token):
    if triger_fb_message(bear, token):
        send_message(bear, token)

