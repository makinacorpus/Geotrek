# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-03-06 13:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_aggregation_infrastructure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='path',
            name='date_update',
            field=models.DateTimeField(auto_now=True, db_column='date_update', db_index=True, verbose_name='Update date'),
        ),
        migrations.AlterField(
            model_name='topology',
            name='date_update',
            field=models.DateTimeField(auto_now=True, db_column='date_update', db_index=True, verbose_name='Update date'),
        ),
    ]
