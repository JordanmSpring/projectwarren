# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0023_auto_20170423_1406'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stockslastdata',
            options={'verbose_name': 'Latest Stocks Data', 'verbose_name_plural': 'Latest Stocks Data'},
        ),
        migrations.AlterField(
            model_name='bannedstocks',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 23, 14, 20, 29, 966895), blank=True),
        ),
        migrations.AlterField(
            model_name='bonds',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 23, 14, 20, 29, 968065), blank=True),
        ),
        migrations.AlterField(
            model_name='guru_and_dividends',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 23, 14, 20, 29, 967365), blank=True),
        ),
        migrations.AlterField(
            model_name='stocks_names',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 23, 14, 20, 29, 965951), blank=True),
        ),
        migrations.AlterField(
            model_name='unworkingstocks',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 23, 14, 20, 29, 966457), blank=True),
        ),
    ]
