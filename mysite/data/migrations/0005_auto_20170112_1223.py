# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_auto_20170112_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stocks_names',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 12, 12, 23, 54, 459220), blank=True),
        ),
        migrations.AlterField(
            model_name='unworkingstocks',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 12, 12, 23, 54, 459726), blank=True),
        ),
        migrations.AlterField(
            model_name='unworkingstocks',
            name='stock',
            field=models.CharField(max_length=10),
        ),
    ]
