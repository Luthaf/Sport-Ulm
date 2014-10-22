# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profilENS', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='occupation',
            field=models.CharField(default='1A', verbose_name='Statut', max_length=3, choices=[('EXT', 'Extérieur'), ('1A', '1A'), ('2A', '2A'), ('3A', '3A'), ('4A', '4A'), ('MAG', 'Magistérien'), ('ARC', 'Archicube'), ('DOC', 'Doctorant'), ('CST', 'CST'), ('PER', 'Personnel ENS')]),
        ),
    ]
