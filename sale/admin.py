from django.contrib import admin
from sale import models


class SaleCategoryModeAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "image_url", "video_url", "status", "start_time", "end_time", "cash_deposit",
                    "commodity_count", "bid_count", "onlook_count", "trading_volume"]
    list_editable = ["title", "status", "image_url", "start_time", "end_time", "cash_deposit",
                     "commodity_count", "bid_count", "onlook_count", "trading_volume"]


class CommodityModeAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "image_url", "salecategory", "video_url", "starting_price", "present_price",
                    "transaction_price", "bid_count", "cash_deposit", "mark_up", "browse_number", "turing_number",
                    "min_price", "max_price",
                    ]
    list_editable = ["title", "image_url", "salecategory", "video_url", "starting_price", "present_price",
                     "transaction_price", "bid_count", "cash_deposit", "mark_up", "browse_number", "turing_number",
                     "min_price", "max_price",
                     ]


class InformationModeAdmin(admin.ModelAdmin):
    list_display = ["id", "commodity", "title", "content"]
    list_editable = ["commodity", "title", "content"]


class CommodityDetailsModeAdmin(admin.ModelAdmin):
    list_display = ["id", "commodity", "status", "image_url"]
    list_editable = ["commodity", "status", "image_url"]


class BidRecordModeAdmin(admin.ModelAdmin):
    list_display = ["id", "bidder", 'bid_time', 'commodity', 'bid_price', 'salecategory']
    list_editable = ["bidder", 'commodity', 'bid_price', 'salecategory']


class CashDepositModeAdmin(admin.ModelAdmin):
    list_display = ["id", "user", 'status', 'guarantee_sum', 'commodity', 'salecategory', ]
    list_editable = ["user", 'status', 'guarantee_sum', 'commodity', 'salecategory', ]


class CareRecordModeAdmin(admin.ModelAdmin):
    list_display = ["id", "user", 'enshrine', 'commodity', 'salecategory', ]
    list_editable = ["user", 'enshrine', 'commodity', 'salecategory']


# Register your models here.
admin.site.register(models.SaleCategory, SaleCategoryModeAdmin)
admin.site.register(models.Commodity, CommodityModeAdmin)
admin.site.register(models.Information, InformationModeAdmin)
admin.site.register(models.CommodityDetails, CommodityDetailsModeAdmin)

admin.site.register(models.BidRecord, BidRecordModeAdmin)

admin.site.register(models.CashDeposit, CashDepositModeAdmin)
admin.site.register(models.CareRecord, CareRecordModeAdmin)
