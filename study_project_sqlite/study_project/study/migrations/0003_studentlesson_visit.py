# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0002_remove_studentlesson_visit'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentlesson',
            name='visit',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
