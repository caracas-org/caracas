# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('character', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField(blank=True, null=True)),
                ('XP_gained', models.PositiveIntegerField()),
                ('icon', models.ImageField(upload_to='', blank=True, null=True)),
                ('max_progress', models.PositiveIntegerField(default=1)),
                ('lon', models.FloatField(blank=True, null=True)),
                ('lat', models.FloatField(blank=True, null=True)),
                ('radius', models.FloatField(help_text='"Activation radius", ie. when you are inside of this radius around lat/lon, the Achievement will unlock', blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AchievementUnlocked',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('progress', models.PositiveIntegerField(default=0)),
                ('started', models.DateTimeField(help_text='When was progress on this achievement started?', auto_now_add=True)),
                ('unlocked', models.DateTimeField(help_text='When was this achievement unlocked (completed).', blank=True, null=True)),
                ('last_progress', models.DateTimeField(auto_now=True)),
                ('achievement', models.ForeignKey(to='achievements.Achievement')),
                ('character', models.ForeignKey(to='character.Character')),
            ],
        ),
    ]
