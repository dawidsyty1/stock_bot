import os
# import logging
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# from datetime import timedelta
# from app import settings

app = Celery('app')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks()
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

