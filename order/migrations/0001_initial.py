# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-07 13:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('books', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name=b'\xe5\x88\xa0\xe9\x99\xa4\xe6\xa0\x87\xe8\xae\xb0')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
                ('count', models.IntegerField(default=1, verbose_name='\u5546\u54c1\u6570\u91cf')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='\u5546\u54c1\u4ef7\u683c')),
                ('books', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Books', verbose_name='\u5546\u54c1\u6570\u91cf')),
            ],
            options={
                'db_table': 's_order_books',
            },
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('is_delete', models.BooleanField(default=False, verbose_name=b'\xe5\x88\xa0\xe9\x99\xa4\xe6\xa0\x87\xe8\xae\xb0')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
                ('order_id', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='\u8ba2\u5355\u7f16\u53f7')),
                ('total_count', models.IntegerField(default=1, verbose_name='\u5546\u54c1\u603b\u6570')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='\u5546\u54c1\u603b\u4ef7')),
                ('transit_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='\u8ba2\u5355\u8fd0\u8d39')),
                ('pay_method', models.SmallIntegerField(choices=[(1, '\u8d27\u5230\u4ed8\u6b3e'), (2, '\u5fae\u4fe1\u652f\u4ed8'), (3, '\u652f\u4ed8\u5b9d'), (4, '\u94f6\u8054\u652f\u4ed8')], default=1, verbose_name='\u8ba2\u5355\u65b9\u5f0f')),
                ('status', models.SmallIntegerField(choices=[(1, '\u5f85\u652f\u4ed8'), (2, '\u5f85\u53d1\u8d27'), (3, '\u5f85\u6536\u8d27'), (4, '\u5f85\u8bc4\u4ef7'), (5, '\u5df2\u5b8c\u6210')], default=1, verbose_name='\u8ba2\u5355\u72b6\u6001')),
                ('trade_id', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='\u652f\u4ed8\u7f16\u53f7')),
                ('addr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Address', verbose_name='\u6536\u8d27\u5730\u5740')),
                ('passport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Passport', verbose_name='\u4e0b\u5355\u8d26\u53f7')),
            ],
            options={
                'db_table': 's_order_info',
            },
        ),
        migrations.AddField(
            model_name='ordergoods',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.OrderInfo', verbose_name='\u6240\u5c5e\u8ba2\u5355'),
        ),
    ]