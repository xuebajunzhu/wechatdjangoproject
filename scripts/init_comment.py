# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/1/15 12:44
import os
import sys
import random
import django

# 添加环境变量
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "auction.settings")

django.setup()  # 读取配置文件
from api import models

user_objs = models.UserInfo.objects.all()
article_objs = models.Article.objects.all()
string = "的是咖啡色大鬼撒会否啊回复i话啊ui发会返回爱国覅给覅噶覅u阿哥覅给覅u阿飞贵啊发给i分别是嗲u戈辉阿哥覅iu啊v看不发达发布啊和哈维杀ui划分方法都是发货服啊和 是"
models.Comment.objects.bulk_create(
    [models.Comment(
        content="".join(random.sample(string, random.randint(1, len(string)))),
        article=random.choice(article_objs),
        commentator=random.choice(user_objs)
    ) for i in range(100)]
)
