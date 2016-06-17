# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rapid', '0003_auto_20150131_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='endDate',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 31, 23, 48, 40, 588389, tzinfo=utc), verbose_name=b'end date of inventory'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inventory',
            name='startDate',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 31, 23, 48, 50, 539764, tzinfo=utc), verbose_name=b'start date of inventory'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='session',
            name='endTime',
            field=models.DateTimeField(auto_now=True, verbose_name=b'end time of session', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='session',
            name='startTime',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'start time of session', null=True),
            preserve_default=True,
        ),
    ]
