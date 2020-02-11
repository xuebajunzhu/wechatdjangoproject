# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/1/19 9:29
from celery.result import AsyncResult
from celery_test import app

async = AsyncResult(id="965a91d6-e21b-4fab-8d0c-a450b7e44d81", app=app)

if async.successful():
    result = async.get()
    print(result)
    # result.forget() # 将结果删除
elif async.failed():
    print('执行失败')
elif async.status == 'PENDING':
    print('任务等待中被执行')
elif async.status == 'RETRY':
    print('任务异常后正在重试')
elif async.status == 'STARTED':
    print('任务已经开始被执行')