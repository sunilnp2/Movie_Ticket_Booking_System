import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qfxcinema.settings")

app = Celery("qfxcinema")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
