# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/2/10 16:49
import datetime
from django.shortcuts import HttpResponse, redirect, render
from django.http import JsonResponse
from web.webModelForm import salecategorymodelform
from sale import models
from web import tasks


def show(request):
    salecategory_objs = models.SaleCategory.objects.all().order_by('-id')
    return render(request, 'web/SaleCategory_show.html', {"salecategory_objs": salecategory_objs})


def addeditor(request, id=None):
    title = "编辑" if id else "添加"
    salecategory_obj = models.SaleCategory.objects.filter(id=id).first()
    if request.method == "GET":
        salecategory_modelformobj = salecategorymodelform.SaleCategorModelForm(instance=salecategory_obj)
        return render(request, "web/salecategory_addeditor.html",
                      {"salecategory_modelformobj": salecategory_modelformobj, "title": title})

    salecategory_modelformobj = salecategorymodelform.SaleCategorModelForm(data=request.POST, instance=salecategory_obj,
                                                                           files=request.FILES)
    if salecategory_modelformobj.is_valid():
        instance = salecategory_modelformobj.save()
        # 1. 从未开始   到 预展
        print(instance.preview_start_time)
        preview_utc_datetime = datetime.datetime.utcfromtimestamp(instance.preview_start_time.timestamp())
        print(preview_utc_datetime)
        preview_task_id = tasks.to_preview_status_task.apply_async(args=[instance.id], eta=preview_utc_datetime).id

        # 2.定时任务，从 预展 到 开拍
        auction_utc_datetime = datetime.datetime.utcfromtimestamp(instance.start_time.timestamp())
        auction_task_id = tasks.to_auction_status_task.apply_async(args=[instance.id], eta=auction_utc_datetime).id

        # 3.定时任务，从 开拍 到 拍卖结束
        auction_end_utc_datetime = datetime.datetime.utcfromtimestamp(instance.end_time.timestamp())
        auction_end_task_id = tasks.end_auction_task.apply_async(args=[instance.id], eta=auction_end_utc_datetime).id

        models.SaleCategory_task.objects.create(
            preview_start_id=preview_task_id,
            start_id=auction_task_id,
            end_start_id=auction_end_task_id,
            salecategory=instance
        )

        return redirect("web:SaleCategory_list")
    return render(request, "web/salecategory_addeditor.html",
                  {"salecategory_modelformobj": salecategory_modelformobj, "title": title})


def delete(request, id):
    models.SaleCategory.objects.filter(id=id).delete()

    return JsonResponse({"status": True})
