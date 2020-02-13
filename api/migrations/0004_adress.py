# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-02-12 10:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_userinfo_open_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('linkman', models.CharField(max_length=48, verbose_name='联系人姓名')),
                ('linkphone', models.CharField(max_length=16, verbose_name='联系人电话')),
                ('address', models.TextField(verbose_name='送货地址')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.UserInfo', verbose_name='用户')),
            ],
        ),
    ]
