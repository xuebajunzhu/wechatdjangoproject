# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-01-17 14:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0007_auto_20200117_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commodity',
            name='max_price',
            field=models.PositiveIntegerField(verbose_name='市场估价最高价'),
        ),
        migrations.AlterField(
            model_name='commodity',
            name='min_price',
            field=models.PositiveIntegerField(verbose_name='市场估价最低价'),
        ),
    ]
