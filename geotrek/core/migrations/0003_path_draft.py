# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-11-14 13:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20180608_1236'),
    ]

    operations = [
        migrations.AddField(
            model_name='path',
            name='draft',
            field=models.BooleanField(db_column='brouillon', default=False, verbose_name='Draft'),
        ),
    ]
