# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bds', '0002_auto_20141102_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sport',
            name='cotisation_frequency',
            field=models.CharField(choices=[('SEM', 'semestre'), ('ANN', 'année'), ('COU', 'cours')], max_length=3, blank=True, null=True, default='ANN', verbose_name='Fréquence de la cotisation'),
        ),
        migrations.AlterField(
            model_name='sport',
            name='price',
            field=models.DecimalField(null=True, decimal_places=2, max_digits=5, verbose_name='Cotisation (€)', blank=True),
        ),
    ]
