from django.db import models


class SaleCategory(models.Model):
    """
    拍卖专场

    首页图片
    首页视频
    title  专场标题
    status 状态 结束  预展中 拍卖中
    starttime 开拍时间
    endtime 结束时间
    拍品数量
    出价次数
    围观次数
    成交额
    全场保证金
    """
    image_url = models.CharField(verbose_name="专场首页图片", max_length=256)
    video_url = models.CharField(verbose_name="专场首页视频", max_length=256, null=True, blank=True)
    title = models.CharField(verbose_name="专场标题", max_length=64)
    status_choice = (
        (1, "预展中"),
        (2, "拍卖中"),
        (3, "已结束")
    )
    status = models.IntegerField(verbose_name="状态", choices=status_choice, default=1)
    start_time = models.DateTimeField(verbose_name="开始时间")
    end_time = models.DateTimeField(verbose_name="结束时间")
    cash_deposit = models.PositiveIntegerField(verbose_name="全场保证金", default=10000)

    commodity_count = models.PositiveIntegerField(verbose_name="拍品数量", default=0)
    bid_count = models.PositiveIntegerField(verbose_name="出价次数", default=0)
    onlook_count = models.PositiveIntegerField(verbose_name="围观次数", default=0)
    trading_volume = models.PositiveIntegerField(verbose_name="成交金额", default=0)

    class Meta:
        verbose_name_plural = "拍卖专场"

    def __str__(self):
        return self.title


class Commodity(models.Model):
    """
    拍品


    专场  foreign key  SaleCategory
    名称 title
    展示图片 image_url
    视频展示 video_url
    起拍价 starting_price
    当前价格 开始等于起拍价 最终等于成交价 present_price
    成交价 开始为空 transaction_price
    出价次数 bid_count
    单品保证金
    加价幅度
    浏览次数
    图录号
    拍品详情介绍
    """
    salecategory = models.ForeignKey(verbose_name="拍卖专场", to="SaleCategory", on_delete=models.CASCADE,
                                     related_name="commodity")
    title = models.CharField(verbose_name="名称", max_length=64)
    image_url = models.CharField(verbose_name="封面", max_length=256)
    video_url = models.CharField(verbose_name="拍品首页视频", max_length=256, null=True, blank=True)

    starting_price = models.PositiveIntegerField(verbose_name="起拍价", default=0)
    present_price = models.PositiveIntegerField(verbose_name="当前出价价格", default=0)
    transaction_price = models.PositiveIntegerField(verbose_name="成交价格", default=0)
    bid_count = models.PositiveIntegerField(verbose_name="出价次数", default=0)
    cash_deposit = models.IntegerField(verbose_name="单品保证金")
    mark_up = models.PositiveIntegerField(verbose_name="加价幅度", default=100)
    browse_number = models.IntegerField(verbose_name="浏览次数", default=0)
    turing_number = models.CharField(verbose_name="图录号", max_length=64)
    particulars = models.TextField(verbose_name="拍品详情介绍")
    min_price = models.PositiveIntegerField(verbose_name="市场估价最低价")
    max_price = models.PositiveIntegerField(verbose_name="市场估价最高价")

    class Meta:
        verbose_name_plural = "拍品"

    def __str__(self):
        return self.title


class Information(models.Model):
    """
    拍品的参数
    一定有一个 市场参考价格

    关联 拍品
    标题
    内容
    """
    commodity = models.ForeignKey(verbose_name="拍品", to="Commodity", on_delete=models.CASCADE)
    title = models.CharField(verbose_name="标题", max_length=32)
    content = models.CharField(verbose_name="内容", max_length=32)

    class Meta:
        verbose_name_plural = "拍品详细参数"

    def __str__(self):
        return self.title


class CommodityDetails(models.Model):
    """
    拍品的详情图片
    status  1 轮播 2详情(1+2)   3详情
    url
    外键关联商品
    """
    commodity = models.ForeignKey(verbose_name="拍品", to="Commodity", on_delete=models.CASCADE)
    status_choice = (
        (1, "轮播图"),
        (2, "详情介绍"),
        (3, "细节描述")
    )
    status = models.IntegerField(verbose_name="图片位置", choices=status_choice)
    image_url = models.CharField(verbose_name="详情图片", max_length=256)

    class Meta:
        verbose_name_plural = "拍品详细图片"


class BidRecord(models.Model):
    """
    出价记录


    出价人
    出价时间
    拍卖的商品  外键Commodity
    价格
    专场   SaleCategory
    """
    bidder = models.ForeignKey(verbose_name="出价者", to="api.UserInfo", related_name="bidder")
    bid_time = models.DateTimeField(verbose_name="出价时间", auto_now_add=True)
    commodity = models.ForeignKey(verbose_name="拍品", to="Commodity", on_delete=models.CASCADE)
    bid_price = models.PositiveIntegerField(verbose_name="出价金额")
    salecategory = models.ForeignKey(verbose_name="所属专场", to="SaleCategory", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "出价记录"


class CashDeposit(models.Model):
    """
    保证金记录
    用户
    status  1 全场保证金   2单场保证金
    金额
    专场 外键
    单个拍品  外键
    """
    user = models.ForeignKey(verbose_name="保证金缴纳者", to="api.UserInfo", related_name="cashd_deposit_user")
    status_choice = (
        (1, "全场保证金"),
        (2, "单品保证金")
    )
    status = models.IntegerField(verbose_name="类型", choices=status_choice)
    guarantee_sum = models.PositiveIntegerField(verbose_name="保证金额")
    commodity = models.ForeignKey(verbose_name="拍品", to="Commodity", on_delete=models.CASCADE, null=True, blank=True)
    salecategory = models.ForeignKey(verbose_name="所属专场", to="SaleCategory", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "保证金缴纳记录"


class CareRecord(models.Model):
    """
    收藏浏览记录
    收藏(默认等于False只是浏览  如果收藏改为True)
    浏览
    """
    user = models.ForeignKey(verbose_name="浏览者", to="api.UserInfo", related_name="carerecord_user")
    enshrine = models.BooleanField(verbose_name="是否收藏", default=False)
    commodity = models.ForeignKey(verbose_name="拍品", to="Commodity", on_delete=models.CASCADE)
    salecategory = models.ForeignKey(verbose_name="所属专场", to="SaleCategory", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "收藏浏览记录"


class Pay_Order(models.Model):
    """
    订单类
    """
    user = models.ForeignKey(verbose_name="用户", to="api.UserInfo", related_name="payorder_user")
    money = models.PositiveIntegerField(verbose_name="金额")
    payment_time = models.DateTimeField(verbose_name="订单创建时间", auto_now_add=True)
    order_number = models.CharField(verbose_name="订单号", null=True, blank=True, max_length=128)
    order_choices = (
        (1, "待支付"),
        (2, "已支付")
    )
    order_status = models.IntegerField(verbose_name="订单状态", choices=order_choices, default=1)
