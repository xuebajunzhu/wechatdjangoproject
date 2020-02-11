# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/1/17 22:37
from rest_framework import serializers
from sale import models


class CommodityModelSerializer(serializers.ModelSerializer):
    starting_price = serializers.SerializerMethodField()
    present_price = serializers.SerializerMethodField()
    transaction_price = serializers.SerializerMethodField()
    care = serializers.SerializerMethodField()
    information = serializers.SerializerMethodField()
    commoditydetails_imageslist = serializers.SerializerMethodField()

    class Meta:
        model = models.Commodity
        fields = ["id", 'title', 'image_url', "video_url", 'present_price', 'transaction_price', 'bid_count',
                  "starting_price", "care", 'mark_up', "browse_number", "min_price", "max_price", "particulars",
                  "turing_number", "information", "commoditydetails_imageslist"]

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
        return "登录后可见"

    def get_care(self, obj):
        request = self.context["request"]
        if request.user:
            care_record_obj = models.CareRecord.objects.filter(user=request.user, commodity=obj)
            if care_record_obj:
                return care_record_obj.enshrine
        return False

    def get_information(self, obj):
        information_objs = obj.information_set.all()
        return [{i.title: i.content} for i in information_objs]

    def get_commoditydetails_imageslist(self, obj):
        commoditydetails_objs = obj.commoditydetails_set.all()
        dic = {}
        for commoditydetails_obj in commoditydetails_objs:
            if commoditydetails_obj.status == 1:
                dic.setdefault("cover", []).append(commoditydetails_obj.image_url)
                dic.setdefault("particulars", []).append(commoditydetails_obj.image_url)
            elif commoditydetails_obj.status == 2:
                dic.setdefault("particulars", []).append(commoditydetails_obj.image_url)
            else:
                dic.setdefault("detail", []).append(commoditydetails_obj.image_url)
        return dic
