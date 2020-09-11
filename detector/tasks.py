from datetime import timedelta, datetime, time
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from detector.models import ActionSettings
from .parser import parse_data
from .fetcher import get_data


@periodic_task(run_every=crontab(hour=15, minute=30))
def task_us_get_data():
    for item in ActionSettings.objects.filter(enable=True):
        get_data(item.symbol, item.token, item.time_resolution)


@periodic_task(run_every=timedelta(seconds=60))
def task_parse_data():
    time = datetime.now().time()
    for item in ActionSettings.objects.filter(enable=True, time_from__gte=time, time_to__lte=time):
        parse_data(item.symbol, item.token, item.time_resolution, item.volume_percenage)

