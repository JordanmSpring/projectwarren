# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0014_auto_20170322_1129'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='guru_and_dividends',
            options={'verbose_name': 'Guru Values and Dividends', 'verbose_name_plural': 'Guru Values and Dividends'},
        ),
        migrations.AlterField(
            model_name='bannedstocks',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 22, 11, 35, 0, 687931), blank=True),
        ),
        migrations.AlterField(
            model_name='bonds',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 22, 11, 35, 0, 689108), blank=True),
        ),
        migrations.AlterField(
            model_name='guru_and_dividends',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 22, 11, 35, 0, 688548), blank=True),
        ),
        migrations.AlterField(
            model_name='stocks_names',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 22, 11, 35, 0, 686960), blank=True),
        ),
        migrations.AlterField(
            model_name='unworkingstocks',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 22, 11, 35, 0, 687460), blank=True),
        ),
    ]
