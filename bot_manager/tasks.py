import logging
from django.db.models.signals import pre_save, post_save
from datetime import timedelta, datetime
from app.celery import app
from django.db.models.signals import pre_save
from django.dispatch import receiver
from celery.decorators import periodic_task
from celery.schedules import crontab
from bot_manager.models import BotSetting
from .parser import check_bot
from .helper import synchronize_time


@app.task
def task_triger_parse_data_for(item_id):
    logging.info('task_triger_parse_data_for {}'.format(item_id))
    item = BotSetting.objects.get(id=item_id)
    if item:
        check_bot(item)


@periodic_task(run_every=crontab(hour=1, minute=00))
def task_parse_data():
    synchronize_time()
    time = datetime.now().time()
    for item in BotSetting.objects.filter(enable=True, time_from__lte=time, time_to__gte=time):
        task_triger_parse_data_for.apply_async(args=(item.id,))




