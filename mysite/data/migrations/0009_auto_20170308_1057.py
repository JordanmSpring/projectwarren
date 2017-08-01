# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0008_auto_20170116_0848'),
    ]

    operations = [
        migrations.AddField(
            model_name='stocks',
            name='price',
            field=models.CharField(max_length=15, blank=True),
        ),
        migrations.AlterField(
            model_name='bannedstocks',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 8, 10, 57, 45, 266587), blank=True),
        ),
        migrations.AlterField(
            model_name='stocks_names',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 8, 10, 57, 45, 265722), blank=True),
        ),
        migrations.AlterField(
            model_name='unworkingstocks',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 8, 10, 57, 45, 266140), blank=True),
        ),
    ]
