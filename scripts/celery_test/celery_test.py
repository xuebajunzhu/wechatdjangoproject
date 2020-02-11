# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/1/19 9:29

import time
from celery import Celery

app = Celery('tasks', broker='redis://192.168.16.198:6381', backend='redis://192.168.16.198:6381')


@app.task
def xxxxxx(x, y):
    time.sleep(10)
    return x + y