# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/1/15 13:00
import os
import sys
import django
#添加环境变量
base_dir = os.path.dirname( os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE","auction.settings")
django.setup()  #读取配置文件