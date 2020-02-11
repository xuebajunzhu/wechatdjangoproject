# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/2/10 16:37

from django.conf.urls import url,include
from web.views.SaleCategory import SaleCategory_show
from web.views.SaleCategory import auction_item_show
urlpatterns = [
    # 专场
    url(r"^SaleCategory/list/$",SaleCategory_show.show,name="SaleCategory_list"),
    url(r"^SaleCategory/add/$",SaleCategory_show.addeditor,name="SaleCategory_add"),
    url(r"^SaleCategory/editor/(\d+)$",SaleCategory_show.addeditor,name="SaleCategory_editor"),
    url(r"^SaleCategory/del/(\d+)$",SaleCategory_show.delete,name="SaleCategory_del"),

    #拍品
    url(r"^auction/list/(?P<salecategory_id>\d+)/$",auction_item_show.show,name="auction_item_list"),
    url(r"^auction/add/(?P<salecategory_id>\d+)/$",auction_item_show.add,name="auction_item_add"),
    url(r"^auction/editor/(?P<salecategory_id>\d+)/(?P<item_id>\d+)/$",auction_item_show.editor,name="auction_item_editor"),
    url(r"^auction/del/(?P<item_id>\d+)/$",auction_item_show.delete,name="auction_item_del"),

    url(r'^auction/item/detail/add/(?P<item_id>\d+)/$', auction_item_show.information_add,
        name='auction_item_detail_add'),
    url(r'^auction/item/detail/add/one/(?P<item_id>\d+)/$', auction_item_show.information_add_one,
        name='auction_item_detail_add_one'),
    url(r'^auction/item/detail/delete/one/$', auction_item_show.auction_item_detail_delete_one,
        name='auction_item_detail_delete_one'),

    url(r'^auction/item/image/add/(?P<item_id>\d+)/$', auction_item_show.auction_item_image_add, name='auction_item_image_add'),
    url(r'^auction/item/image/add/one/(?P<item_id>\d+)/$', auction_item_show.auction_item_image_add_one,
        name='auction_item_image_add_one'),
    url(r'^auction/item/image/delete/one/$', auction_item_show.auction_item_image_delete_one,
        name='auction_item_image_delete_one'),

]
