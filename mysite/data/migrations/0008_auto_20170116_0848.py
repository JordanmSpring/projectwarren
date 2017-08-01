# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0007_auto_20170112_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='stocks',
            name='exchange',
            field=models.CharField(max_length=150, blank=True),
        ),
        migrations.AddField(
            model_name='stocks',
            name='name',
            field=models.CharField(max_length=150, blank=True),
        ),
        migrations.AlterField(
            model_name='bannedstocks',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 16, 8, 48, 2, 815845), blank=True),
        ),
        migrations.AlterField(
            model_name='stocks_names',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 16, 8, 48, 2, 814932), blank=True),
        ),
        migrations.AlterField(
            model_name='unworkingstocks',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 16, 8, 48, 2, 815391), blank=True),
        ),
    ]
