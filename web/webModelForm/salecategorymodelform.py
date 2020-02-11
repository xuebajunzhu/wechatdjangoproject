# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/2/10 17:31
from sale import models
from django import  forms


class SaleCategorModelForm(forms.ModelForm):
    class Meta:
        model = models.SaleCategory
        fields = "__all__"
        exclude = ["commodity_count", "bid_count", "onlook_count", "trading_volume"]
        labels = {
            "image_url": "专场首页图片",
            "title": "专场标题",
            "satus": "状态",
            "start_time": "开始时间",
            "end_time": "结束时间",
            "cash_deposit": "全场保证金"
        }
        widgets={
            "start_time":forms.TextInput(attrs={"type":'data'}),
            "end_time":forms.TextInput(attrs={"type":'data'})
        }

    def __init__(self, *args, **kwargs):
        super(SaleCategorModelForm, self).__init__(*args, **kwargs)
        for field_name, item in self.fields.items():
            item.widget.attrs.update({"class": "form-control"})
