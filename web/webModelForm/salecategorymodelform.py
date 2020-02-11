# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/2/10 17:31
import uuid
from utils.tencent.cos import upload_file
from sale import models
from django import forms
from django.db.models.fields.files import FieldFile


class BootstrapModelForm(forms.ModelForm):
    exclude_bootstrap_class = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, item in self.fields.items():
            old_class = item.widget.attrs.get("class", "")
            if field_name in self.exclude_bootstrap_class:
                continue
            item.widget.attrs["class"] = old_class + " form-control"


class SaleCategorModelForm(BootstrapModelForm):
    exclude_bootstrap_class = ["image_url"]

    class Meta:
        model = models.SaleCategory
        fields = "__all__"
        exclude = ["commodity_count", "bid_count", "onlook_count", "trading_volume", "video_url"]
        labels = {
            "image_url": "专场首页图片",
            "title": "专场标题",
            "satus": "状态",
            "preview_start_time": "预展时间",
            "start_time": "开始时间",
            "end_time": "结束时间",
            "cash_deposit": "全场保证金"
        }
        # widgets = {
        #     "image_url": forms.TextInput(attrs={"type": "file"}),
        #     "start_time": forms.TextInput(attrs={"type": 'data'}),
        #     "end_time": forms.TextInput(attrs={"type": 'data'})
        # }

    def clean(self):
        # 获取用户提交的文件对象

        cleaned_data = self.cleaned_data
        print(cleaned_data)
        obj = cleaned_data.get("image_url")
        if not obj:
            return cleaned_data

        # 将对象上传到腾讯云
        # 返回得到文件地址
        ext = obj.name.rsplit('.', maxsplit=1)[-1]

        file_name = "{0}.{1}".format(str(uuid.uuid4()), ext)
        cleaned_data['image_url'] = upload_file(obj, file_name)
        return cleaned_data


class AuctionItemAddModelForm(BootstrapModelForm):
    exclude_bootstrap_class = ['image_url']

    class Meta:
        model = models.Commodity
        exclude = ['salecategory', 'turing_number', 'status', 'transaction_price', 'video_url', 'bid_count',
                   'browse_number']

    def clean(self):
        cleaned_data = self.cleaned_data
        # 上传文件
        cover_file_object = cleaned_data.get('cover')
        if not cover_file_object or isinstance(cover_file_object, FieldFile):
            return cleaned_data
        ext = cover_file_object.name.rsplit('.', maxsplit=1)[-1]
        file_name = "{0}.{1}".format(str(uuid.uuid4()), ext)
        cleaned_data['cover'] = upload_file(cover_file_object, file_name)
        return cleaned_data


class AuctionItemEditModelForm(BootstrapModelForm):
    exclude_bootstrap_class = ['cover']

    class Meta:
        model = models.Commodity
        exclude = ['auction', 'turing_number', 'status', 'transaction_price', 'video_url', 'bid_count', 'look_count']

    def clean(self):
        cleaned_data = self.cleaned_data
        # 上传文件
        cover_file_object = cleaned_data.get('cover')
        if not cover_file_object or isinstance(cover_file_object, FieldFile):
            return cleaned_data
        ext = cover_file_object.name.rsplit('.', maxsplit=1)[-1]
        file_name = "{0}.{1}".format(str(uuid.uuid4()), ext)
        cleaned_data['cover'] = upload_file(cover_file_object, file_name)
        return cleaned_data


class InformationModelForm(forms.ModelForm):
    class Meta:
        model = models.Information
        exclude = ['commodity']


class AuctionItemImageModelForm(BootstrapModelForm):
    class Meta:
        model = models.CommodityDetails
        exclude = ['commodity',"status"]


    def clean(self):
        cleaned_data = self.cleaned_data
        # 上传文件
        cover_file_object = cleaned_data.get('img')
        if not cover_file_object or isinstance(cover_file_object, FieldFile):
            return cleaned_data

        ext = cover_file_object.name.rsplit('.', maxsplit=1)[-1]
        file_name = "{0}.{1}".format(str(uuid.uuid4()), ext)
        cleaned_data['img'] = upload_file(cover_file_object, file_name)
        return cleaned_data
