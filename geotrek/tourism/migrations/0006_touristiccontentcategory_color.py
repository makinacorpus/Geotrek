# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-06-25 16:48
from __future__ import unicode_literals

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tourism', '0005_auto_20190328_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='touristiccontentcategory',
            name='color',
            field=colorfield.fields.ColorField(db_column='couleur', default='#444444', max_length=18, verbose_name='Color (mobile app only)'),
        ),
    ]
