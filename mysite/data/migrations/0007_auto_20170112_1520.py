# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0006_auto_20170112_1517'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bannedstocks',
            options={'verbose_name': 'Banned Stocks', 'verbose_name_plural': 'Banned Stocks'},
        ),
        migrations.AlterField(
            model_name='bannedstocks',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 12, 15, 20, 31, 680013), blank=True),
        ),
        migrations.AlterField(
            model_name='stocks_names',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 12, 15, 20, 31, 679070), blank=True),
        ),
        migrations.AlterField(
            model_name='unworkingstocks',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 12, 15, 20, 31, 679541), blank=True),
        ),
    ]
