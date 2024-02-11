import os

from celery import Celery

# celery -A Wurmple worker --loglevel info -E -- Run Celery Task

os.environ.setdefault("CONNECTION_MAX_AGE", "0")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
celery_app = Celery("Wurmple")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()
