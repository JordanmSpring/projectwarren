# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='stocks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stock', models.CharField(max_length=10)),
                ('date', models.CharField(max_length=25)),
                ('scraperError', models.CharField(max_length=250, blank=True)),
                ('scraperApi', models.CharField(max_length=250, blank=True)),
                ('bookValue', models.CharField(max_length=12, blank=True)),
                ('debtEquitity', models.CharField(max_length=12, blank=True)),
                ('priceEarning', models.CharField(max_length=12, blank=True)),
                ('operatingCashFlow', models.CharField(max_length=12, blank=True)),
                ('leveredCashFlow', models.CharField(max_length=12, blank=True)),
                ('priceEarningGrowth', models.CharField(max_length=12, blank=True)),
                ('acquirersMultiple', models.CharField(max_length=12, blank=True)),
                ('capitalmarket', models.CharField(max_length=12, blank=True)),
                ('freecashflow', models.CharField(max_length=12, blank=True)),
                ('freecashflowpercent', models.CharField(max_length=12, blank=True)),
            ],
            options={
                'verbose_name': 'Stocks Data',
                'verbose_name_plural': 'Stocks Data',
            },
        ),
        migrations.CreateModel(
            name='stocks_names',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stock', models.CharField(unique=True, max_length=10)),
                ('date', models.DateTimeField(default=datetime.datetime(2017, 1, 3, 10, 52, 11, 498696), blank=True)),
            ],
            options={
                'verbose_name': 'Stocks',
                'verbose_name_plural': 'Stocks',
            },
        ),
    ]
