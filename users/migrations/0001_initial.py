# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-07 13:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name=b'\xe5\x88\xa0\xe9\x99\xa4\xe6\xa0\x87\xe8\xae\xb0')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
                ('recipient_name', models.CharField(max_length=20, verbose_name='\u6536\u4ef6\u4eba')),
                ('recipient_addr', models.CharField(max_length=256, verbose_name='\u6536\u4ef6\u5730\u5740')),
                ('zip_code', models.CharField(max_length=6, verbose_name='\u90ae\u653f\u7f16\u7801')),
                ('recipient_phone', models.CharField(max_length=11, verbose_name='\u8054\u7cfb\u7535\u8bdd')),
                ('is_default', models.BooleanField(default=False, verbose_name='\u8d26\u6237')),
            ],
            options={
                'db_table': 's_user_address',
            },
        ),
        migrations.CreateModel(
            name='Passport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name=b'\xe5\x88\xa0\xe9\x99\xa4\xe6\xa0\x87\xe8\xae\xb0')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
                ('username', models.CharField(max_length=20, verbose_name='\u7528\u6237\u540d\u79f0')),
                ('password', models.CharField(max_length=40, verbose_name='\u5bc6\u7801')),
                ('email', models.EmailField(max_length=254, verbose_name='\u7528\u6237\u90ae\u7bb1')),
                ('is_active', models.BooleanField(default=False, verbose_name='\u6fc0\u6d3b\u72b6\u6001')),
            ],
            options={
                'db_table': 's_user_account',
            },
        ),
        migrations.AddField(
            model_name='address',
            name='passport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Passport', verbose_name='\u8d26\u6237'),
        ),
    ]
