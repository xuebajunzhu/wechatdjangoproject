# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/1/17 22:35
from sale import models
from rest_framework.generics import ListAPIView, RetrieveAPIView
from sale.serializer.commodity import CommodityModelSerializer


class CommodityView(RetrieveAPIView):
    queryset = models.Commodity.objects
    serializer_class = CommodityModelSerializer
