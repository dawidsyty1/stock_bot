from .parser import parse_backtest_data
from .fetcher import grab_data_backtest
from .models import BotSetting
from app.celery import app
import time
import logging
# @app.task
# def task_triger_parse_data_for(item_id):
#     logging.info('task_triger_parse_data_for {}'.format(item_id))
#     item = BotSetting.objects.get(id=item_id)
#     if item:
#         check_bot(item)


# @periodic_task(run_every=crontab(hour=1, minute=00))
# def task_parse_data():
#     synchronize_time()
#     time = datetime.now().time()
#     for item in BotSetting.objects.filter(enable=True, time_from__lte=time, time_to__gte=time):
#         task_triger_parse_data_for.apply_async(args=(item.id,))


@app.task
def task_make_backtest():
    for days_back in range(100, 0, -1):
        for item in BotSetting.objects.filter(enable=True, strategy__backtest=True):
            print('start name', item.name, days_back)
            try:
                time.sleep(1)
                grab_data_backtest(item, days_back)
                print('start parser', days_back)
                parse_backtest_data(item, days_back)
            except Exception as error:
                print('Error: ', days_back, error)





