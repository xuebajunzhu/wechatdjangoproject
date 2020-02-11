# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/2/10 16:37

from django.conf.urls import url,include
from web.views.SaleCategory import SaleCategory_show

urlpatterns = [
    url(r"^SaleCategory/list/$",SaleCategory_show.show,name="SaleCategory_list"),
    url(r"^SaleCategory/add/$",SaleCategory_show.addeditor,name="SaleCategory_add"),
    url(r"^SaleCategory/editor/(\d+)$",SaleCategory_show.addeditor,name="SaleCategory_editor"),
    url(r"^SaleCategory/del/(\d+)$",SaleCategory_show.delete,name="SaleCategory_del"),
]
