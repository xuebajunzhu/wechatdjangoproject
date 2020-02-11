# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/1/19 9:29

import celery_test

# 立即告知celery去执行xxxxxx任务，并传入两个参数
result = celery_test.xxxxxx.delay(4, 4)
print(result.id)
