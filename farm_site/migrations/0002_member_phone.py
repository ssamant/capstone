# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-07 17:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm_site', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='phone',
            field=models.CharField(default='206-555-5555', max_length=12),
        ),
    ]