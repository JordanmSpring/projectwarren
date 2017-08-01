# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0016_auto_20170322_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bannedstocks',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 22, 11, 40, 28, 409748), blank=True),
        ),
        migrations.AlterField(
            model_name='bonds',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 22, 11, 40, 28, 410918), blank=True),
        ),
        migrations.AlterField(
            model_name='guru_and_dividends',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 22, 11, 40, 28, 410318), blank=True),
        ),
        migrations.AlterField(
            model_name='stocks_names',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 22, 11, 40, 28, 408786), blank=True),
        ),
        migrations.AlterField(
            model_name='unworkingstocks',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 22, 11, 40, 28, 409286), blank=True),
        ),
    ]
