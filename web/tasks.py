# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/2/12 10:12

import uuid
import datetime
import itertools
from celery import shared_task
from sale import models
from utils.encrypt import md5


@shared_task
def to_preview_status_task(auction_id):
    print("预展开始了")
    models.SaleCategory.objects.filter(id=auction_id).update(status=2)
    models.Commodity.objects.filter(salecategory_id=auction_id).update(status=2)
    print("to_preview_status_task结束了")


@shared_task
def to_auction_status_task(auction_id):
    print("拍卖开始了")
    models.SaleCategory.objects.filter(id=auction_id).update(status=3)
    models.Commodity.objects.filter(salecategory_id=auction_id).update(status=3)
    print("to_auction_status_task结束了")


@shared_task
def end_auction_task(auction_id):
    print("拍卖结束了")
    models.SaleCategory.objects.filter(id=auction_id).update(status=4)
    models.Commodity.objects.filter(salecategory_id=auction_id).update(status=4)
    print("end_auction_task结束了")

    # 判断每个拍品的最高价,以及是否出价,没有人出价则流拍
    total = 0
    total_unfortunate_list = []
    lucky_auction_deposit_id = set()
    auction_object = models.SaleCategory.objects.filter(id=auction_id).first()
    item_object_list = models.Commodity.objects.filter(salecategory=auction_object)
    # 循环所有拍品
    for item_object in item_object_list:
        # 获取当前最高价
        lucky_object = models.BidRecord.objects.filter(commodity=item_object).order_by('-bid_price').first()

        # 无出价,则流派
        if not lucky_object:
            item_object.status = 5
            item_object.save()
            continue
        lucky_object.status = 2
        lucky_object.save()
        # 拍品设置成交价:
        item_object.transaction_price = lucky_object.bid_price
        item_object.save()
        # 专场成交总额
        total += lucky_object.bid_price

        # 获取当前用户为此拍品缴纳的保证金(单品/全场)对象
        deposit_object = models.CashDeposit.objects.filter(
            user=lucky_object.bidder,
            commodity=item_object,
            status=1).first()
        if not deposit_object:
            # deposit_object
            deposit_object = models.CashDeposit.objects.filter(user=lucky_object.bidder,
                                                               salecategory=auction_object,
                                                               status=2, commodity__isnull=True).first()
            # 所有已经拍到的人缴纳的保证金记录的id
        lucky_auction_deposit_id.add(deposit_object.id)
        # 生成订单
        order_object = models.Pay_Order.objects.create(
            uid=md5(uuid.uuid4()),
            user=lucky_object.bidder,
            commodity=item_object,
            deposit=deposit_object,  # 单品或者专场保证金的记录
            due_money=lucky_object.bid_price,
        )
        # 单品保证金: 所有没有拍到的商品 & 缴纳的是单品保证金记录
        item_unfortunate_list = models.CashDeposit.objects.filter(commodity=item_object, status=1).exclude(
            user=lucky_object.bidder)
        total_unfortunate_list.extend(item_unfortunate_list)
        # 调用定时任务:24小时内要支付,否则流派 扣除保证金
        date = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        task_id = twenty_four_hour.apply_async(args=[order_object.id],
                                               eta=date).id
        order_object.twenty_four_task_id = task_id
        order_object.save()
    # 专场:更新成交额
    auction_object.trading_volume = total
    auction_object.save()

    # 未拍到任何商品的用户的全场保证金
    auction_unfortunate_list = models.CashDeposit.objects.filter(
        status=2,
        salecategory=auction_object,
        commodity__isnull=True).exclude(id__in=lucky_auction_deposit_id)
    # 退保证金(原路退还)
    for deposit in itertools.chain(total_unfortunate_list, auction_unfortunate_list):
        uid = md5(uuid.uuid4())
        if deposit.pay_type == 1:  # 微信
            # res = refund(uid, deposit.uid, deposit.amount, deposit.amount)
            res = True
            models.DepositRefundRecord.objects.create(
                uid=uid,
                status=2 if res else 1,
                amount=deposit.guarantee_sum,
                deposit=deposit
            )
            if res:
                deposit.margin_balance = 0
                deposit.save()
        else:  # 余额
            deposit.user.balance += deposit.amount
            deposit.user.save()
            models.DepositRefundRecord.objects.create(
                uid=uid,
                status=2,
                amount=deposit.guarantee_sum,
                deposit=deposit
            )
            deposit.margin_balance = 0
            deposit.save()


@shared_task
def twenty_four_hour(order_id):
    """ 24小时不支付订单,则直接扣除保证金 """
    print("处理未支付的订单")
    # 订单已支付
    order_object = models.Pay_Order.objects.filter(id=order_id).first()
    if order_object.status != 1:
        return
    # 订单状态为 逾期未付款
    order_object.status = 4
    order_object.save()
    # 单品保证金 直接扣除
    if order_object.deposit.status == 1:
        order_object.deposit.margin_balance = 0
        order_object.deposit.save()
        models.DepositDeduct.objects.create(order=order_object, amount=order_object.deposit.guarantee_sum)
        return
    # 全场保证金,扣除部分保证金(如果有剩余,则检查是否还有其他订单,如果没有则剩余保证金直接返回到原账户)
    """
        情景一:
            全场保证金:1000
                A:9000 200 扣除200 退还800
            全场保证金:1000
                A 9000 200 扣除200
                B 800 400  扣除400 退还400
            全场保证金:1000
                A 9000 200 扣除200
                B 9000 900 扣除800 退还0
    
    """
    if order_object.deposit.margin_balance <= order_object.commodity.cash_deposit:
        models.DepositDeduct.objects.create(order=order_object,
                                            amount=order_object.deposit.margin_balance)
        order_object.deposit.margin_balance = 0
        order_object.deposit.save()
        return
    order_object.deposit.margin_balance -= order_object.commodity.cash_deposit
    order_object.deposit.save()
    models.DepositDeduct.objects.create(order=order_object,
                                        amount=order_object.commodity.cash_deposit)
    # 检查此专场保证金下是否还有其他的订单未支付
    exists = models.Pay_Order.objects.filter(user=order_object.user, status=1,
                                             commodity__salecategory=order_object.deposit.salecategory).\
                                            exclude(id=order_id).exists()
    if exists:
        return
    uid = md5(uuid.uuid4())
    if order_object.deposit.pay_type == 1:  # 微信
        # res = refund(uid, deposit.uid, deposit.amount, deposit.amount)
        res = True
        models.DepositRefundRecord.objects.create(
            uid=uid,
            status=2 if res else 1,
            amount=order_object.deposit.margin_balance,
            deposit=order_object.deposit
        )
        if res:
            order_object.deposit.margin_balance = 0
            order_object.deposit.save()
    else:  # 余额
        order_object.deposit.user.balance += order_object.deposit.margin_balance
        order_object.deposit.user.save()
        models.DepositRefundRecord.objects.create(
            uid=uid,
            status=2,
            amount=order_object.deposit.margin_balance,
            deposit=order_object.deposit
        )
        order_object.deposit.margin_balance = 0
        order_object.deposit.save()
