from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

from envparse import env

env.read_envfile()

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')

app.conf.broker_url = f'amqp://{env.str("RABBITMQ_USER")}:{env.str("RABBITMQ_PASS")}@{env.str("RABBITMQ_HOST")}:{env.str("RABBITMQ_PORT")}/'

# Using a string here means the worker doesn't have to serialize
app.conf.beat_schedule = {
    'fetch-albums-every-hour': {
        'schedule': crontab(minute='0'),
        'task': 'backend_service.tasks.albums_fetcher_task',
        'args': ()
    }
}
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
