# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/1/9 11:02

from rest_framework import serializers
from api.seriralizer.validators import phone_validator
from rest_framework.exceptions import ValidationError
from django_redis import get_redis_connection
class MessageSerializers(serializers.Serializer):
    phone = serializers.CharField(label="手机号", validators=[phone_validator, ])


class LoginSerializers(serializers.Serializer):
    phone = serializers.CharField(label="手机号", validators=[phone_validator, ])
    code = serializers.CharField(label="验证码", max_length=4, min_length=4)

    def validated_code(self, value):
        if len(value) != 4 or value.isdecimal():
            raise ValidationError("验证码格式错误")
        phone = self.initial_data.get("phone")
        conn = get_redis_connection("default")
        redis_code = conn.get(phone)
        print("redis_code",redis_code)
        if not redis_code:
            raise ValidationError("验证码不存在")
        elif redis_code.decode("utf-8") != value:
            raise ValidationError("验证码错误")
