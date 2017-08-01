# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0021_auto_20170403_0826'),
    ]

    operations = [
        migrations.CreateModel(
            name='stocksLastData',
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
                ('roic', models.CharField(max_length=12, blank=True)),
                ('capitalmarket', models.CharField(max_length=12, blank=True)),
                ('freecashflow', models.CharField(max_length=12, blank=True)),
                ('freecashflowpercent', models.CharField(max_length=12, blank=True)),
                ('exchange', models.CharField(max_length=150, blank=True)),
                ('name', models.CharField(max_length=150, blank=True)),
                ('price', models.CharField(max_length=15, blank=True)),
                ('dcf_value', models.CharField(max_length=15, blank=True)),
                ('safety_margin', models.CharField(max_length=15, blank=True)),
            ],
            options={
                'verbose_name': 'Stocks Data',
                'verbose_name_plural': 'Stocks Data',
            },
        ),
        migrations.AlterField(
            model_name='bannedstocks',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 23, 14, 5, 11, 377381), blank=True),
        ),
        migrations.AlterField(
            model_name='bonds',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 23, 14, 5, 11, 378476), blank=True),
        ),
        migrations.AlterField(
            model_name='guru_and_dividends',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 23, 14, 5, 11, 377829), blank=True),
        ),
        migrations.AlterField(
            model_name='stocks_names',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 23, 14, 5, 11, 376348), blank=True),
        ),
        migrations.AlterField(
            model_name='unworkingstocks',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 23, 14, 5, 11, 376900), blank=True),
        ),
    ]
