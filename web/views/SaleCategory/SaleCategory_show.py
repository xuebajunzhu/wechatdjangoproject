# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/2/10 16:49
from django.shortcuts import HttpResponse, redirect, render
from django.http import JsonResponse
from web.webModelForm import salecategorymodelform
from sale import models


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

    salecategory_modelformobj = salecategorymodelform.SaleCategorModelForm(data=request.POST, instance=salecategory_obj,files=request.FILES)
    if salecategory_modelformobj.is_valid():
        salecategory_modelformobj.save()
        return redirect("web:SaleCategory_list")
    return render(request, "web/salecategory_addeditor.html",
                  {"salecategory_modelformobj": salecategory_modelformobj, "title": title})


def delete(request, id):
    obj = models.SaleCategory.objects.filter(id=id)
    print(obj)
    return JsonResponse({"status":True})
