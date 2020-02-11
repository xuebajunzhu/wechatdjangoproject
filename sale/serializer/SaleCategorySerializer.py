# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/1/17 15:05

from rest_framework import serializers
from sale import models


class SaleCategoryModelSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    end_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    status = serializers.CharField(source="get_status_display")
    commodity_image_list = serializers.SerializerMethodField()

    class Meta:
        model = models.SaleCategory
        # fields = ["commodity_image_list", "id", "image_url", "title", 'status', 'commodity_count', "onlook_count",
        #           "bid_count",'start_time', 'end_time', "trading_volume"]
        exclude = ["video_url", "cash_deposit"]

    def get_commodity_image_list(self, obj):
        commodity_objs = obj.commodity.all()
        obj.Commodity_count = commodity_objs.count()
        obj.save()
        return [i.image_url for i in commodity_objs]


class CommodityModelSerializer(serializers.ModelSerializer):
    starting_price = serializers.SerializerMethodField()
    present_price = serializers.SerializerMethodField()
    transaction_price = serializers.SerializerMethodField()
    care = serializers.SerializerMethodField()

    class Meta:
        model = models.Commodity
        fields = ["id", 'title', 'image_url', 'present_price', 'transaction_price', 'bid_count', "starting_price",
                  "care",'mark_up', "browse_number","min_price","max_price"]

    def get_starting_price(self, obj):
        request = self.context["request"]
        if request.user:
            return obj.starting_price
        return "登录后可见"

    def get_present_price(self, obj):
        request = self.context["request"]
        if request.user:
            return obj.present_price
        return "登录后可见"

    def get_transaction_price(self, obj):
        request = self.context["request"]
        if request.user:
            return obj.transaction_price

    def get_care(self, obj):
        request = self.context["request"]
        if request.user:
            care_record_obj = models.CareRecord.objects.filter(user=request.user, commodity=obj)
            if care_record_obj:
                return care_record_obj.enshrine
        return False


# class SaleCategoryDetialModelSerializer(SaleCategoryModelSerializer):
#     commodity = CommodityModelSerializer(many=True)


class SaleCategoryDetialModelSerializer(serializers.ModelSerializer):
    commodity = CommodityModelSerializer(many=True)
    start_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    end_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    status = serializers.CharField(source="get_status_display")

    class Meta:
        model = models.SaleCategory
        # fields = ["commodity_image_list", "id", "image_url", "title", 'status', 'Commodity_count', "onlook_count",
        #           "bid_count",'start_time', 'end_time', "trading_volume"]
        exclude = ["video_url", "cash_deposit"]


