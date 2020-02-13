# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/2/11 17:34
import datetime
import uuid
import json
from django.shortcuts import HttpResponse, redirect, render, reverse
from django.http import JsonResponse
from web.webModelForm import salecategorymodelform
from django.views.decorators.csrf import csrf_exempt
from sale import models
from utils.tencent.cos import upload_file


def show(request, salecategory_id):
    salecategory_obj = models.SaleCategory.objects.filter(id=salecategory_id).first()
    commodity_list = models.Commodity.objects.filter(salecategory=salecategory_obj)
    return render(request, 'web/auction_item_show.html',
                  {"salecategory_obj": salecategory_obj, "commodity_list": commodity_list})


@csrf_exempt
def add(request, salecategory_id):
    salecategory_obj = models.SaleCategory.objects.filter(id=salecategory_id).first()
    if request.method == "GET":
        form = salecategorymodelform.AuctionItemAddModelForm()
        return render(request, "web/auction_item_add.html", {"salecategory_obj": salecategory_obj, "form": form})
    print(request.POST)
    form = salecategorymodelform.AuctionItemAddModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.instance.salecategory = salecategory_obj
        form.instance.turing_number = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        instance = form.save()

        return JsonResponse({
            'status': True,
            'data': {
                'detail_url': reverse('web:auction_item_detail_add', kwargs={'item_id': instance.id}),
                'image_url': reverse('web:auction_item_image_add', kwargs={'item_id': instance.id}),
                'list_url': reverse('web:auction_item_list', kwargs={'salecategory_id': salecategory_id})
            }
        })

    return JsonResponse({'status': False, 'errors': form.errors})


def editor(request, salecategory_id,item_id):
    item_object = models.Commodity.objects.filter(id=item_id).first()
    detail_object_list = models.Information.objects.filter(commodity=item_object)
    image_object_list = models.CommodityDetails.objects.filter(commodity=item_object)
    context = {
        "item_object": item_object,
        "detail_object_list": detail_object_list,
        "image_object_list": image_object_list
    }

    if request.method == 'GET':
        form = salecategorymodelform.AuctionItemAddModelForm(instance=item_object)
    else:
        form = salecategorymodelform.AuctionItemAddModelForm(instance=item_object, data=request.POST,
                                                             files=request.FILES)
        if form.is_valid():
            form.save()
    context['form'] = form
    return render(request, 'web/auction_item_editor.html', context)


def delete(request, item_id):
    models.Commodity.objects.filter(id=item_id).delete()
    return JsonResponse({'status': True})


@csrf_exempt
def information_add(request, item_id):
    """
    创建规格
    待处理**
    :param request:
    :return:
    """
    detail_list = json.loads(request.body.decode('utf-8'))
    print(detail_list)
    object_list = [models.Information(**info, commodity_id=item_id) for info in detail_list if all(info.values())]
    models.Information.objects.bulk_create(object_list)
    return JsonResponse({'status': True})


@csrf_exempt
def information_add_one(request, item_id):
    """
    添加规则
    :param request:
    :param item_id:
    :return:
    """
    if request.method != 'POST':
        return JsonResponse({'status': False})
    form = salecategorymodelform.InformationModelForm(data=request.POST)
    if form.is_valid():
        form.instance.commodity_id = item_id
        instance = form.save()
        return JsonResponse({'status': True, 'data': {'id': instance.id}})
    return JsonResponse({'status': False, 'errors': form.errors})


@csrf_exempt
def auction_item_detail_delete_one(request):
    detail_id = request.GET.get('detail_id')
    models.Information.objects.filter(id=detail_id).delete()
    return JsonResponse({'status': True})


@csrf_exempt
def auction_item_image_add(request, item_id):
    """
    创建图片 待处理
    :param request:
    :param item_id:
    :return:
    """
    show_list = request.POST.getlist('show')
    image_object_list = request.FILES.getlist('img')

    orm_object_list = []
    for index in range(len(image_object_list)):
        image_object = image_object_list[index]
        if not image_object:
            continue
        ext = image_object.name.rsplit('.', maxsplit=1)[-1]
        file_name = "{0}.{1}".format(str(uuid.uuid4()), ext)
        cos_path = upload_file(image_object, file_name)
        print(cos_path)
        orm_object_list.append(models.CommodityDetails(image_url=cos_path, commodity_id=item_id, status=bool(show_list[index])))
    if orm_object_list:
        models.CommodityDetails.objects.bulk_create(orm_object_list)
    return JsonResponse({'status': True})


@csrf_exempt
def auction_item_image_add_one(request, item_id):
    status = {"status":request.POST.get("status")[0]}
    form = salecategorymodelform.AuctionItemImageModelForm(data=status, files=request.FILES)
    if form.is_valid():
        form.instance.commodity_id = item_id
        instance = form.save()
        return JsonResponse({'status': True, 'data': {'id': instance.id}})
    return JsonResponse({'status': False, 'errors': form.errors})


def auction_item_image_delete_one(request):
    image_id = request.GET.get('image_id')
    models.CommodityDetails.objects.filter(id=image_id).delete()
    return JsonResponse({'status': True})
