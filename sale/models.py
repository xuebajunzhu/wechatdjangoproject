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
    # FileField = 数据保存文件路径CharField + ModelForm显示时File来生成标签 + ModelForm.save()
    image_url = models.FileField(verbose_name="专场首页图片", max_length=256)
    video_url = models.CharField(verbose_name="专场首页视频", max_length=256, null=True, blank=True)
    title = models.CharField(verbose_name="专场标题", max_length=64)
    status_choice = (
        (1, "未开始"),
        (2, "预展中"),
        (3, "拍卖中"),
        (4, "已结束"),

    )
    status = models.IntegerField(verbose_name="状态", choices=status_choice, default=1)
    preview_start_time = models.DateTimeField(verbose_name="预展时间", null=True, blank=True)
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
class SaleCategory_task(models.Model):
    salecategory = models.OneToOneField(verbose_name="拍卖专场", to="SaleCategory", on_delete=models.CASCADE,
                                     related_name="salecategory_task")
    preview_start_id = models.CharField(verbose_name="预展任务id",max_length=128,null=True,blank=True)
    start_id = models.CharField(verbose_name="预展任务id",max_length=128,null=True,blank=True)
    end_start_id = models.CharField(verbose_name="预展任务id",max_length=128,null=True,blank=True)

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
    image_url = models.FileField(verbose_name="封面", max_length=256)
    video_url = models.CharField(verbose_name="拍品首页视频", max_length=256, null=True, blank=True)
    status_choices = (
        (1, '未开拍'),
        (2, '预展中'),
        (3, '拍卖中'),
        (4, '成交'),
        (5, '流拍'),
        (6, '逾期未付款'),
    )
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=status_choices, default=1)

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
    image_url = models.FileField(verbose_name="详情图片", max_length=256)

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
    status_choices = (
        (1, '竞价'),
        (2, '成交'),
        (3, '逾期未付款'),
    )
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=status_choices, default=1)
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
        (2, "全场保证金"),
        (1, "单品保证金")
    )
    status = models.IntegerField(verbose_name="类型", choices=status_choice)
    guarantee_sum = models.PositiveIntegerField(verbose_name="保证金额")
    margin_balance = models.PositiveIntegerField(verbose_name="保证金余额")
    pay_type_choices = (
        (1, '微信'),
        (2, '余额')
    )
    pay_type = models.SmallIntegerField(verbose_name='支付方式', choices=pay_type_choices)

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
    commodity = models.ForeignKey(verbose_name="拍品", to="Commodity")
    due_money = models.PositiveIntegerField(verbose_name="应付金额")
    payment = models.PositiveIntegerField(verbose_name="实际付款金额")
    payment_time = models.DateTimeField(verbose_name="订单创建时间", auto_now_add=True)
    deposit = models.ForeignKey(verbose_name='保证金', to='CashDeposit')
    order_number = models.CharField(verbose_name="订单号", null=True, blank=True, max_length=128)
    twenty_four_task_id = models.CharField(verbose_name='24小时后的定时任务id',
                                           max_length=32, null=True, blank=True)
    order_choices = (
        (1, "待支付"),
        (2, "代收货"),
        (3, "已完成"),
        (4, "逾期未付款"),
    )
    order_status = models.IntegerField(verbose_name="订单状态", choices=order_choices, default=1)
    address = models.OneToOneField(verbose_name="送货地址",to="api.Adress",on_delete=models.CASCADE)

class DepositRefundRecord(models.Model):
    """保证金退款记录"""
    uid = models.CharField(verbose_name="流水号",max_length=64)
    status_choices = (
        (1, "待退款"),
        (2, '已退款'),
    )
    status = models.PositiveSmallIntegerField(verbose_name='状态',
                                              choices=status_choices)
    deposit = models.ForeignKey(verbose_name='保证金', to='CashDeposit')
    amount = models.PositiveIntegerField(verbose_name='退款金额')

class DepositDeduct(models.Model):
    """扣除保证金"""
    order = models.ForeignKey(verbose_name='订单', to='Pay_Order')
    amount = models.PositiveIntegerField(verbose_name='金额')

class Couponcash(models.Model):
    """
    优惠券

    关联用户
    关联订单
    某一专场(有值不通用  ,没有值就是通用的)
    优惠金额
    优惠限制(满多少钱可以使用)
    状态(有效,过期,已使用)
    有效期(开始时间 失效时间)
    """
    user= models.ForeignKey(verbose_name="领取用户",to="api.UserInfo",null=True,blank=True)
    pay_order = models.ForeignKey(verbose_name="订单",to=Pay_Order,null=True,blank=True)
    salecategory = models.ForeignKey(verbose_name="专场",to="SaleCategory",null=True,blank=True)

    discount_money=models.PositiveIntegerField(verbose_name="优惠金额")
    limit_money = models.PositiveIntegerField(verbose_name="满足金额",null=True,blank=True)
    status_choise=(
        (1,"有效"),
        (2,"过期"),
        (3,"已使用")
    )
    status=models.PositiveIntegerField(verbose_name="优惠券状态",choices=status_choise,default=1)
    create_time=models.DateTimeField(verbose_name="有效期起始日期",auto_now_add=True)
    end_time=models.DateTimeField(verbose_name="失效日期")



