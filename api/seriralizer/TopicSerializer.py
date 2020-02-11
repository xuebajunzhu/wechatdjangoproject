# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/1/12 14:31
from api import models
from rest_framework import serializers


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model= models.Topic
        fields = "__all__"
