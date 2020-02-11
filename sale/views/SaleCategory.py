# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/1/17 14:46
from sale import models
from rest_framework.generics import ListAPIView, RetrieveAPIView

from sale.serializer.SaleCategorySerializer import SaleCategoryModelSerializer, SaleCategoryDetialModelSerializer
from rest_framework.pagination import LimitOffsetPagination


class SaleCategoryLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 1
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 20


class SaleCategoryListView(ListAPIView):
    queryset = models.SaleCategory.objects.all().order_by("-id")
    serializer_class = SaleCategoryModelSerializer
    pagination_class = SaleCategoryLimitOffsetPagination

    def get_queryset(self):

        print(self.request.query_params)
        min_id = self.request.query_params.get("min_id")
        print(min_id)
        max_id = self.request.query_params.get("max_id")
        if min_id:
            return models.SaleCategory.objects.filter(id__lt=min_id).order_by("-id")
        elif max_id:
            return models.SaleCategory.objects.filter(id__gt=max_id).order_by("id")
        else:
            return models.SaleCategory.objects.all().order_by("-id")


class SaleCategoryView(RetrieveAPIView):
    serializer_class = SaleCategoryDetialModelSerializer
    queryset = models.SaleCategory.objects
