# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-02-11 10:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import geotrek.authent.models


class Migration(migrations.Migration):

    dependencies = [
        ('signage', '0009_auto_20191029_1110'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='signagetype',
            options={'ordering': ('label',), 'verbose_name': 'Signage Type', 'verbose_name_plural': 'Signage Types'},
        ),
        migrations.AlterField(
            model_name='blade',
            name='color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='signage.Color', verbose_name='Color'),
        ),
        migrations.AlterField(
            model_name='blade',
            name='condition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='infrastructure.InfrastructureCondition', verbose_name='Condition'),
        ),
        migrations.AlterField(
            model_name='blade',
            name='direction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='signage.Direction', verbose_name='Direction'),
        ),
        migrations.AlterField(
            model_name='blade',
            name='number',
            field=models.CharField(max_length=250, verbose_name='Number'),
        ),
        migrations.AlterField(
            model_name='blade',
            name='signage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='signage.Signage', verbose_name='Signage'),
        ),
        migrations.AlterField(
            model_name='blade',
            name='structure',
            field=models.ForeignKey(default=geotrek.authent.models.default_structure_pk, on_delete=django.db.models.deletion.CASCADE, to='authent.Structure', verbose_name='Related structure'),
        ),
        migrations.AlterField(
            model_name='blade',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signage.BladeType', verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='bladetype',
            name='label',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='bladetype',
            name='structure',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authent.Structure', verbose_name='Related structure'),
        ),
        migrations.AlterField(
            model_name='color',
            name='label',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='direction',
            name='label',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='line',
            name='blade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='lines', to='signage.Blade', verbose_name='Blade'),
        ),
        migrations.AlterField(
            model_name='line',
            name='distance',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True, verbose_name='Distance'),
        ),
        migrations.AlterField(
            model_name='line',
            name='number',
            field=models.IntegerField(verbose_name='Number'),
        ),
        migrations.AlterField(
            model_name='line',
            name='pictogram_name',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Pictogramm name'),
        ),
        migrations.AlterField(
            model_name='line',
            name='structure',
            field=models.ForeignKey(default=geotrek.authent.models.default_structure_pk, on_delete=django.db.models.deletion.CASCADE, to='authent.Structure', verbose_name='Related structure'),
        ),
        migrations.AlterField(
            model_name='line',
            name='text',
            field=models.CharField(max_length=1000, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='line',
            name='time',
            field=models.DurationField(blank=True, help_text='Hours:Minutes:Seconds', null=True, verbose_name='Time'),
        ),
        migrations.AlterField(
            model_name='sealing',
            name='label',
            field=models.CharField(max_length=250, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='sealing',
            name='structure',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authent.Structure', verbose_name='Related structure'),
        ),
        migrations.AlterField(
            model_name='signage',
            name='code',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='signage',
            name='condition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='infrastructure.InfrastructureCondition', verbose_name='Condition'),
        ),
        migrations.AlterField(
            model_name='signage',
            name='description',
            field=models.TextField(blank=True, help_text='Specificites', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='signage',
            name='eid',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='External id'),
        ),
        migrations.AlterField(
            model_name='signage',
            name='implantation_year',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Implantation year'),
        ),
        migrations.AlterField(
            model_name='signage',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.Organism', verbose_name='Manager'),
        ),
        migrations.AlterField(
            model_name='signage',
            name='name',
            field=models.CharField(help_text='Reference, code, ...', max_length=128, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='signage',
            name='printed_elevation',
            field=models.IntegerField(blank=True, null=True, verbose_name='Printed elevation'),
        ),
        migrations.AlterField(
            model_name='signage',
            name='sealing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='signage.Sealing', verbose_name='Sealing'),
        ),
        migrations.AlterField(
            model_name='signage',
            name='structure',
            field=models.ForeignKey(default=geotrek.authent.models.default_structure_pk, on_delete=django.db.models.deletion.CASCADE, to='authent.Structure', verbose_name='Related structure'),
        ),
        migrations.AlterField(
            model_name='signage',
            name='topo_object',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.Topology'),
        ),
        migrations.AlterField(
            model_name='signage',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signage.SignageType', verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='signagetype',
            name='label',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='signagetype',
            name='structure',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authent.Structure', verbose_name='Related structure'),
        ),
        migrations.AlterField(
            model_name='blade',
            name='deleted',
            field=models.BooleanField(default=False, editable=False, verbose_name='Deleted'),
        ),
        migrations.AlterModelTable(
            name='blade',
            table=None,
        ),
        migrations.AlterModelTable(
            name='bladetype',
            table=None,
        ),
        migrations.AlterModelTable(
            name='color',
            table=None,
        ),
        migrations.AlterModelTable(
            name='direction',
            table=None,
        ),
        migrations.AlterModelTable(
            name='line',
            table=None,
        ),
        migrations.AlterModelTable(
            name='sealing',
            table=None,
        ),
        migrations.AlterModelTable(
            name='signage',
            table=None,
        ),
        migrations.AlterModelTable(
            name='signagetype',
            table=None,
        ),
    ]
