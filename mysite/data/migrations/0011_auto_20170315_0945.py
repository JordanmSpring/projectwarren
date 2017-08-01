# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0010_auto_20170312_1708'),
    ]

    operations = [
        migrations.CreateModel(
            name='bonds',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('australian_bond', models.CharField(unique=True, max_length=10)),
                ('american_bond', models.CharField(unique=True, max_length=10)),
                ('date', models.DateTimeField(default=datetime.datetime(2017, 3, 15, 9, 45, 36, 692126), blank=True)),
            ],
            options={
                'verbose_name': 'Bonds',
                'verbose_name_plural': 'Bonds',
            },
        ),
        migrations.AlterField(
            model_name='bannedstocks',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 15, 9, 45, 36, 690945), blank=True),
        ),
        migrations.AlterField(
            model_name='guru_and_dividends',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 15, 9, 45, 36, 691562), blank=True),
        ),
        migrations.AlterField(
            model_name='stocks_names',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 15, 9, 45, 36, 690018), blank=True),
        ),
        migrations.AlterField(
            model_name='unworkingstocks',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 15, 9, 45, 36, 690485), blank=True),
        ),
    ]
