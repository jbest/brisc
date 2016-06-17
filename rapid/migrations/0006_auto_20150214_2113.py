# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rapid', '0005_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='inventory_ID',
        ),
        migrations.AddField(
            model_name='taxonset',
            name='note',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taxonset',
            name='startTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 15, 3, 13, 10, 134317, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='session',
            name='endTime',
            field=models.DateTimeField(null=True, verbose_name=b'end time of session', blank=True),
            preserve_default=True,
        ),
    ]
