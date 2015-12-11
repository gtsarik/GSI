# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-10 16:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import gsi.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gsi', '0002_tiletype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('run_parallel', models.BooleanField(default=False)),
                ('mode', models.CharField(max_length=50)),
                ('input_file', models.CharField(max_length=200)),
                ('output_tile_subdir', models.CharField(max_length=200)),
                ('input_scale_factor', models.CharField(max_length=200)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gsi.Area')),
            ],
            options={
                'verbose_name_plural': 'Collate cards',
            },
            bases=(gsi.utils.UnicodeNameMixin, models.Model),
        ),
        migrations.CreateModel(
            name='MergeCSV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('csv1', models.CharField(max_length=200)),
                ('csv2', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
            bases=(gsi.utils.UnicodeNameMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PreProc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('run_parallel', models.BooleanField(default=False)),
                ('mode', models.CharField(max_length=50)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gsi.Area')),
                ('year_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gsi.YearGroup')),
            ],
            options={
                'verbose_name_plural': 'PreProc cards',
            },
            bases=(gsi.utils.UnicodeNameMixin, models.Model),
        ),
        migrations.CreateModel(
            name='QRF',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('interval', models.CharField(max_length=100)),
                ('number_of_trees', models.IntegerField(default=0)),
                ('number_of_threads', models.IntegerField(default=1)),
                ('directory', models.CharField(max_length=300)),
            ],
            options={
                'verbose_name_plural': 'QRF cards',
            },
            bases=(gsi.utils.UnicodeNameMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Remap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('run_parallel', models.BooleanField(default=False)),
                ('file_spec', models.CharField(max_length=200)),
                ('roi', models.CharField(max_length=200)),
                ('output_root', models.CharField(max_length=200)),
                ('output_suffix', models.CharField(max_length=200)),
                ('scale', models.CharField(max_length=200)),
                ('output', models.CharField(max_length=200)),
                ('color_table', models.CharField(max_length=200)),
                ('refstats_file', models.CharField(max_length=200)),
                ('refstats_scale', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Remap cards',
            },
            bases=(gsi.utils.UnicodeNameMixin, models.Model),
        ),
        migrations.CreateModel(
            name='RFScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('run_parallel', models.BooleanField(default=False)),
                ('bias_corrn', models.CharField(max_length=200)),
                ('number_of_threads', models.IntegerField(default=1)),
                ('QRFopts', models.CharField(max_length=300)),
                ('ref_target', models.CharField(max_length=100)),
                ('clean_name', models.CharField(max_length=100)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gsi.Area')),
                ('year_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gsi.YearGroup')),
            ],
            options={
                'verbose_name_plural': 'RFScore cards',
            },
            bases=(gsi.utils.UnicodeNameMixin, models.Model),
        ),
        migrations.CreateModel(
            name='RFTrain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('run_parallel', models.BooleanField(default=False)),
                ('number_of_trees', models.IntegerField(default=0)),
                ('value', models.CharField(max_length=300)),
                ('config_file', models.CharField(max_length=200)),
                ('output_tile_subdir', models.CharField(max_length=200)),
                ('input_scale_factor', models.CharField(max_length=200)),
                ('tile_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gsi.TileType')),
            ],
            options={
                'abstract': False,
            },
            bases=(gsi.utils.UnicodeNameMixin, models.Model),
        ),
        migrations.CreateModel(
            name='YearFilter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('run_parallel', models.BooleanField(default=False)),
                ('filetype', models.CharField(max_length=50)),
                ('filter', models.CharField(max_length=200)),
                ('filter_output', models.CharField(max_length=300)),
                ('extend_start', models.CharField(max_length=200)),
                ('input_fourier', models.CharField(max_length=200)),
                ('output_directory', models.CharField(max_length=300)),
                ('input_directory', models.CharField(max_length=200)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gsi.Area')),
            ],
            options={
                'verbose_name_plural': 'YearFilter cards',
            },
            bases=(gsi.utils.UnicodeNameMixin, models.Model),
        ),
    ]
