# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/1/19 11:08
from celery import shared_task

@shared_task
def add(x, y):
    return x + y

@shared_task
def mul(x, y):
    return x * y