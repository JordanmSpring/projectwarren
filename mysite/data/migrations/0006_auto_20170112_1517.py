# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_auto_20170112_1223'),
    ]

    operations = [
        migrations.CreateModel(
            name='bannedStocks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stock', models.CharField(unique=True, max_length=10)),
                ('date', models.DateTimeField(default=datetime.datetime(2017, 1, 12, 15, 17, 34, 941270), blank=True)),
            ],
            options={
                'verbose_name': 'Unworking Stocks',
                'verbose_name_plural': 'Unworking Stocks',
            },
        ),
        migrations.AlterField(
            model_name='stocks_names',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 12, 15, 17, 34, 940334), blank=True),
        ),
        migrations.AlterField(
            model_name='unworkingstocks',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 12, 15, 17, 34, 940794), blank=True),
        ),
    ]
