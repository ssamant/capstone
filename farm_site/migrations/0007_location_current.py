# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-08 06:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm_site', '0006_signup'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='current',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]