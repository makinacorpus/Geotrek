# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-12-18 15:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infrastructure', '0004_auto_20181113_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseinfrastructure',
            name='eid',
            field=models.CharField(blank=True, db_column='id_externe', max_length=128, null=True, verbose_name='External id'),
        ),
    ]
