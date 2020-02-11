# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/1/9 11:03
import re
from rest_framework.exceptions import ValidationError


def phone_validator(value):  # 返回None 验证通过   失败  抛出异常
    if not re.match(r"^(1[3|4|5|6|7|8|9])\d{9}$", value):
        raise ValidationError("手机格式错误")
