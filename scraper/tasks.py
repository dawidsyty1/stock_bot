import logging
from app.celery import app
from app import settings
from scraper import models, scrapers


@app.task
def _run_task(task_id):
    """
    Service new task by Celery.
    """
    logging.info("Executing new task {}".format(task_id))

    task = models.Task.objects.get(id=task_id)
    task.set_as_inprogress()

    scraper = scrapers.ScraperFactory.get_scraper(task.type)
    try:
        scraper.download_content(task.url)
        scraper.retrieve_resources(task)
        task.set_as_succeed()
    except scrapers.ScraperBaseError as error:
        logging.error(error)
        task.set_as_abandoned()
    start_unfinish_tasks()


def start_unfinish_tasks():
    """
    Restart broken/suspend tasks.
    """
    logging.info("Starting faid tasks")

    tasks = models.Task.objects.exclude(status='abandoned').exclude(status='succeed')

    for task in tasks:
        if task.is_to_abandon():
            _run_task(task.id)
        else:
            task.set_as_abandoned()


def start_new_task(task_id):
    """
    Start new task in two mods.
    """
    logging.info("Starting new task in {} mode".format(
        "asynchronous" if settings.ASYNCHRONOUS_ON is True else "normal")
    )

    if settings.ASYNCHRONOUS_ON:
        result = _run_task.delay(task_id)

    else:
        _run_task(task_id)
