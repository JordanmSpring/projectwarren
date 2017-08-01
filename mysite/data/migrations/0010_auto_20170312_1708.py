# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0009_auto_20170308_1057'),
    ]

    operations = [
        migrations.CreateModel(
            name='guru_and_dividends',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stock', models.CharField(unique=True, max_length=10)),
                ('date', models.DateTimeField(default=datetime.datetime(2017, 3, 12, 17, 8, 17, 929683), blank=True)),
                ('cost_of_capital', models.CharField(unique=True, max_length=10)),
                ('dividend', models.CharField(unique=True, max_length=10)),
                ('dividend_five_years', models.CharField(unique=True, max_length=10)),
            ],
            options={
                'verbose_name': 'Cost of Capital and Dividends',
                'verbose_name_plural': 'Cost of Capital and Dividends',
            },
        ),
        migrations.AlterField(
            model_name='bannedstocks',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 12, 17, 8, 17, 929121), blank=True),
        ),
        migrations.AlterField(
            model_name='stocks_names',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 12, 17, 8, 17, 928217), blank=True),
        ),
        migrations.AlterField(
            model_name='unworkingstocks',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 12, 17, 8, 17, 928669), blank=True),
        ),
    ]
