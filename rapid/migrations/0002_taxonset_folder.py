# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rapid', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxonset',
            name='folder',
            field=models.ForeignKey(to='rapid.FolderType', null=True),
            preserve_default=True,
        ),
    ]
