import os

from celery import Celery
from celery.schedules import crontab
from celery.signals import worker_ready
from glob import glob

from blog import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
TASKS_FILES = map(lambda x: x.replace('/tasks.py', '').replace('/', '.'), glob('**/tasks.py', recursive=True))

celery_app = Celery('blog', broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks(TASKS_FILES, force=True)

celery_app.conf.beat_schedule = {
    'delete-inactive-users': {
        'task': 'users.delete-inactive-users',
        'schedule': 3600 * 48
    }
}


@worker_ready.connect
def setup_periodic_tasks(sender: Celery, **kwargs) -> None:
    # if app_config.DEBUG:
    celery_app.send_task('users.delete-inactive-users')
