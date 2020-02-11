# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/1/18 10:07
from sale import models
from rest_framework.generics import RetrieveAPIView
from sale.serializer.cashdeposit import CommodityCashDepositModelSerializer


class CommodityCashDepositView(RetrieveAPIView):
    queryset = models.Commodity.objects
    serializer_class = CommodityCashDepositModelSerializer
