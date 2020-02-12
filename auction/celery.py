# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/1/19 11:03

import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auction.settings')  #项目同名目录下的settings

app = Celery('auction')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
# 去每个已注册app中读取 tasks.py 文件
app.autodiscover_tasks()