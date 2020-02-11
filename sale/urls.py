# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/1/17 13:29
from django.conf.urls import url
from sale.views import SaleCategory
from sale.views import commodity
from sale.views import cashdeposit
from sale.views import celery_test
import hashlib
urlpatterns = [
    url(r"^salecategory/$",SaleCategory.SaleCategoryListView.as_view()),
    url(r"^salecategory/(?P<pk>\d+)/$",SaleCategory.SaleCategoryView.as_view()),
    url(r"^commodity/(?P<pk>\d+)/$",commodity.CommodityView.as_view()),
    url(r"^cashdeposit/(?P<pk>\d+)/$",cashdeposit.CommodityCashDepositView.as_view()),


    ####celery测试
    url(r'^create/task/$', celery_test.create_task),
    url(r'^get/result/$', celery_test.get_result),
]