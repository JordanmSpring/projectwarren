# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0011_auto_20170315_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bannedstocks',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 15, 12, 31, 17, 408631), blank=True),
        ),
        migrations.AlterField(
            model_name='bonds',
            name='american_bond',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='bonds',
            name='australian_bond',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='bonds',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 15, 12, 31, 17, 409745), blank=True),
        ),
        migrations.AlterField(
            model_name='guru_and_dividends',
            name='cost_of_capital',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='guru_and_dividends',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 15, 12, 31, 17, 409178), blank=True),
        ),
        migrations.AlterField(
            model_name='guru_and_dividends',
            name='dividend',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='guru_and_dividends',
            name='dividend_five_years',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='guru_and_dividends',
            name='stock',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='stocks_names',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 15, 12, 31, 17, 407684), blank=True),
        ),
        migrations.AlterField(
            model_name='unworkingstocks',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 15, 12, 31, 17, 408154), blank=True),
        ),
    ]
