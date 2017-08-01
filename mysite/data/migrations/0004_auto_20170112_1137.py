# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_auto_20170104_1540'),
    ]

    operations = [
        migrations.CreateModel(
            name='unworkingStocks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stock', models.CharField(unique=True, max_length=10)),
                ('date', models.DateTimeField(default=datetime.datetime(2017, 1, 12, 11, 37, 3, 184456), blank=True)),
            ],
            options={
                'verbose_name': 'Unworking Stocks',
                'verbose_name_plural': 'Unworking Stocks',
            },
        ),
        migrations.AlterField(
            model_name='stocks_names',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 12, 11, 37, 3, 183978), blank=True),
        ),
    ]
