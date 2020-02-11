# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/1/19 11:12

from django.shortcuts import HttpResponse
from sale.tasks import add
import datetime
def create_task(request):
    print('请求来了')
    ctime = datetime.datetime.now()
    utc_ctime = datetime.datetime.utcfromtimestamp(ctime.timestamp())

    s10 = datetime.timedelta(seconds=10)
    ctime_x = utc_ctime + s10

    # 使用apply_async并设定时间
    result = add.apply_async(args=[1, 3], eta=ctime_x)


    # result = add.delay(2,2)

    print('执行完毕')
    return HttpResponse(result.id)


def get_result(request):
    nid = request.GET.get('nid')
    from celery.result import AsyncResult
    # from demos.celery import app
    from auction import app
    result_object = AsyncResult(id=nid, app=app)
    # print(result_object.status)
    data = result_object.get()
    return HttpResponse(data)