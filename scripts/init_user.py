# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/1/15 13:01
from scripts import django_setting

from api import models

message = []
for i in range(20):
    message.append(models.Message.objects.create())

models.UserInfo.objects.bulk_create(
    [models.UserInfo(
        phone=f"{i}18864803318",
        nickName=f"{i}cqk",
        avatarUrl="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJCnOwWmSnwAEDnMqc4L8gq1cmfsY6ZlXtMXuur7QegRPlOViaWuZDrtlhwWmicJCuLlqYtgbSZS9ww/132",
        message=message[i],
        token="1f4a3fe0-4f97-45d3-b36d-b01135f0b8cd"
    ) for i in range(20)]
)
