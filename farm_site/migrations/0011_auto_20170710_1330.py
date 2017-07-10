# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-10 20:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm_site', '0010_auto_20170710_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='signup',
            name='box',
            field=models.CharField(choices=[('regular', 'Regular'), ('large', 'Large')], default='regular', max_length=7),
        ),
        migrations.AddField(
            model_name='signup',
            name='eggs',
            field=models.CharField(choices=[('none', 'None'), ('half-dozen', 'Half Dozen'), ('dozen', 'Dozen')], default='none', max_length=10),
        ),
    ]