# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-17 23:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('david', '0011_standing'),
    ]

    operations = [
        migrations.AddField(
            model_name='standing',
            name='matchesPlayed',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
