# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-02-12 03:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0013_auto_20200211_1925'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaleCategory_task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preview_start_id', models.CharField(blank=True, max_length=128, null=True, verbose_name='预展任务id')),
                ('start_id', models.CharField(blank=True, max_length=128, null=True, verbose_name='预展任务id')),
                ('end_start_id', models.CharField(blank=True, max_length=128, null=True, verbose_name='预展任务id')),
            ],
        ),
        migrations.AlterField(
            model_name='salecategory',
            name='status',
            field=models.IntegerField(choices=[(1, '未开始'), (2, '预展中'), (3, '拍卖中'), (4, '已结束')], default=1, verbose_name='状态'),
        ),
        migrations.AddField(
            model_name='salecategory_task',
            name='salecategory',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='salecategory_task', to='sale.SaleCategory', verbose_name='拍卖专场'),
        ),
    ]
