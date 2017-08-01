# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0022_auto_20170423_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bannedstocks',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 23, 14, 6, 47, 359795), blank=True),
        ),
        migrations.AlterField(
            model_name='bonds',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 23, 14, 6, 47, 360933), blank=True),
        ),
        migrations.AlterField(
            model_name='guru_and_dividends',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 23, 14, 6, 47, 360269), blank=True),
        ),
        migrations.AlterField(
            model_name='stocks_names',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 23, 14, 6, 47, 358743), blank=True),
        ),
        migrations.AlterField(
            model_name='unworkingstocks',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 23, 14, 6, 47, 359271), blank=True),
        ),
    ]
