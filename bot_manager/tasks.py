from .models import BotSetting
from config.celery import app
from celery.schedules import crontab
from celery.task import periodic_task
from strategies.ema_crossover import ema_crossover

@app.task
async def backtest_ema_crossover_task(symbol):
    await ema_crossover(symbol)


@periodic_task(run_every=crontab(hour=1, minute=00))
def task_parse_data():
    for item in BotSetting.objects.filter():
        backtest_ema_crossover_task.delay(item.symbol)




