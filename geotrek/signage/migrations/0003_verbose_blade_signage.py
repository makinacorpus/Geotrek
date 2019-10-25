# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-01-29 14:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('signage', '0002_permissions_signage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blade',
            name='color',
            field=models.ForeignKey(blank=True, db_column='couleur', null=True, on_delete=django.db.models.deletion.PROTECT, to='signage.Color', verbose_name='Color'),
        ),
        migrations.AlterField(
            model_name='line',
            name='time',
            field=models.DurationField(blank=True, db_column='temps', help_text='Hours:Minutes:Seconds', null=True, verbose_name='Time'),
        ),
        migrations.AlterField(
            model_name='signage',
            name='printed_elevation',
            field=models.IntegerField(blank=True, db_column='altitude_imprimee', null=True, verbose_name='Printed elevation'),
        ),
        migrations.AlterModelOptions(
            name='bladetype',
            options={'verbose_name': 'Blade type', 'verbose_name_plural': 'Blade types'},
        ),
        migrations.AlterModelOptions(
            name='color',
            options={'verbose_name': 'Blade color', 'verbose_name_plural': 'Blade colors'},
        ),
    ]
