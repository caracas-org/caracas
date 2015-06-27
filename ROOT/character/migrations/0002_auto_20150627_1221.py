# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('character', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='lat',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='character',
            name='lon',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
