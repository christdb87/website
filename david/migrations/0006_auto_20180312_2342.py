# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-13 03:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('david', '0005_pointtotal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pointtotal',
            name='matchday',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='david.Fixture'),
        ),
    ]
