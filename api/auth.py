# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/1/16 10:14
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from api import models


class Auth(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        if not token:
            return None
        user_obj = models.UserInfo.objects.filter(token=token)
        if not user_obj:
            return None
        return (user_obj, token)


class CoerceAuth(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        if not token:
            raise AuthenticationFailed("用户未登录")
            # return None
        user_obj = models.UserInfo.objects.filter(token=token)
        if not user_obj:
            raise AuthenticationFailed("token有问题请重新登录")
            # return None
        return (user_obj, token)
