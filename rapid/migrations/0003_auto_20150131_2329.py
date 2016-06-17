# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rapid', '0002_session_inventory_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='endTime',
            field=models.DateTimeField(null=True, verbose_name=b'end time of session', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='session',
            name='startTime',
            field=models.DateTimeField(null=True, verbose_name=b'start time of session', blank=True),
            preserve_default=True,
        ),
    ]
