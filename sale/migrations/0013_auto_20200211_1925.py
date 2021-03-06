# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-02-11 11:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0012_commodity_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commodity',
            name='image_url',
            field=models.FileField(max_length=256, upload_to='', verbose_name='封面'),
        ),
        migrations.AlterField(
            model_name='commoditydetails',
            name='image_url',
            field=models.FileField(max_length=256, upload_to='', verbose_name='详情图片'),
        ),
    ]
