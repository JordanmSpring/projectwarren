# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0013_auto_20170318_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='guru_and_dividends',
            name='intrinsic_value',
            field=models.CharField(max_length=10, blank=True),
        ),
        migrations.AlterField(
            model_name='bannedstocks',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 22, 11, 29, 34, 936436), blank=True),
        ),
        migrations.AlterField(
            model_name='bonds',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 22, 11, 29, 34, 937665), blank=True),
        ),
        migrations.AlterField(
            model_name='guru_and_dividends',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 22, 11, 29, 34, 937028), blank=True),
        ),
        migrations.AlterField(
            model_name='stocks_names',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 22, 11, 29, 34, 935465), blank=True),
        ),
        migrations.AlterField(
            model_name='unworkingstocks',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 22, 11, 29, 34, 935968), blank=True),
        ),
    ]
