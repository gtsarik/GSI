# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_auto_20170108_2121'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shelfdata',
            options={'verbose_name_plural': 'Shelf Data'},
        ),
    ]
