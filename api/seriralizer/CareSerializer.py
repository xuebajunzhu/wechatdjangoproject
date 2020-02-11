# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/1/16 11:47
from rest_framework import serializers
from api import models


class CareSerializer(serializers.ModelSerializer):
    attention = serializers.SerializerMethodField()

    class Meta:
        model = models.Message
        fields = ["attention"]

    def get_attention(self, obj):
        pass
