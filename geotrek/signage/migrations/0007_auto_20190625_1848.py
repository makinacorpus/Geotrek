# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-06-25 16:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signage', '0006_auto_20190306_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blade',
            name='number',
            field=models.CharField(db_column='numero', max_length=250, verbose_name='Number'),
        ),
    ]
