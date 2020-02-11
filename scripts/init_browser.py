# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/1/15 12:45

import os
import sys
import django
#添加环境变量
base_dir = os.path.dirname( os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE","auction.settings")
django.setup()  #读取配置文件

from api import models
user_id = models.UserInfo.objects.all().values("id")

artciledetial_objs = models.ArticleDetail.objects.all()
for i in artciledetial_objs:
    i.browse_user.add(*[i["id"] for i in user_id])
    i.browse_count = i.browse_user.count()

