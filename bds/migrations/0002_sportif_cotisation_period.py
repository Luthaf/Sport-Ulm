# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bds', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sportif',
            name='cotisation_period',
            field=models.CharField(verbose_name='Inscription', max_length=3, choices=[('ANN', 'Année'), ('SE1', 'Premier semestre'), ('SE2', 'Deuxième semestre')], default='ANN'),
            preserve_default=True,
        ),
    ]
