from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Job_Application.settings')

app = Celery('Job_Application')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
app.conf.worker_pool_restarts = True
app.conf.broker_connection_retry_on_startup = True

app.conf.beat_schedule = {
    'run-my-periodic-task': {
        'task': 'Company.tasks.update_company_data',
        'schedule': crontab(minute='*/3600'),
    },
}
