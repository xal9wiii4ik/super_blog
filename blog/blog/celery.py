import os

from celery import Celery
from glob import glob

from blog import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
TASKS_FILES = map(lambda x: x.replace('/tasks.py', '').replace('/', '.'), glob('**/tasks.py', recursive=True))

celery_app = Celery('blog', broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks(TASKS_FILES, force=True)