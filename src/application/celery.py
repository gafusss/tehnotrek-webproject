from __future__ import absolute_import
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')

from django.conf import settings

capp = Celery('application')
capp.config_from_object('django.conf:settings')
capp.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
