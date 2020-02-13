# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/1/18 10:11


# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/1/17 22:37
from rest_framework import serializers
from sale import models


class  CommodityCashDepositModelSerializer(serializers.ModelSerializer):

    global_cash_deposit =serializers.IntegerField(source="salecategory.cash_deposit")
    # image_url = serializers.CharField()#由于django的ORM是FileField字段,所有drf自动生成了FileField字段,带本地前缀+数据库值
    image_url = serializers.CharField()#把默认的 FileField 改成CharField
    class Meta:
        model = models.Commodity
        fields = ["id", 'title', 'image_url', "min_price", "max_price", "cash_deposit","global_cash_deposit","starting_price","salecategory"]


