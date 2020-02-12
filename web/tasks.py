# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/2/12 10:12

import uuid
from celery import shared_task
from sale import models


@shared_task
def to_preview_status_task(auction_id):
    print("to_preview_status_task开始了")
    models.SaleCategory.objects.filter(id=auction_id).update(status=2)
    models.Commodity.objects.filter(salecategory_id=auction_id).update(status=2)
    print("to_preview_status_task结束了")


@shared_task
def to_auction_status_task(auction_id):
    print("to_auction_status_task开始了")
    models.SaleCategory.objects.filter(id=auction_id).update(status=3)
    models.Commodity.objects.filter(salecategory_id=auction_id).update(status=3)
    print("to_auction_status_task结束了")

@shared_task
def end_auction_task(auction_id):
    print("end_auction_task开始了")
    models.SaleCategory.objects.filter(id=auction_id).update(status=4)
    models.Commodity.objects.filter(salecategory_id=auction_id).update(status=4)
    print("end_auction_task结束了")