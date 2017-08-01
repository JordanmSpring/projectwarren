# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0019_auto_20170326_1014'),
    ]

    operations = [
        migrations.AddField(
            model_name='stocks',
            name='dcf_value',
            field=models.CharField(max_length=15, blank=True),
        ),
        migrations.AddField(
            model_name='stocks',
            name='safety_margin',
            field=models.CharField(max_length=15, blank=True),
        ),
        migrations.AlterField(
            model_name='bannedstocks',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 26, 12, 11, 9, 596277), blank=True),
        ),
        migrations.AlterField(
            model_name='bonds',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 26, 12, 11, 9, 597357), blank=True),
        ),
        migrations.AlterField(
            model_name='guru_and_dividends',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 26, 12, 11, 9, 596758), blank=True),
        ),
        migrations.AlterField(
            model_name='stocks_names',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 26, 12, 11, 9, 595189), blank=True),
        ),
        migrations.AlterField(
            model_name='unworkingstocks',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 26, 12, 11, 9, 595720), blank=True),
        ),
    ]
