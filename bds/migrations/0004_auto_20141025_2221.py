# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bds', '0003_auto_20141024_1611'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventoption',
            options={'verbose_name': 'Option'},
        ),
        migrations.AlterField(
            model_name='sport',
            name='cotisation_frequency',
            field=models.CharField(blank=True, choices=[('SEM', 'Semestrielle'), ('ANN', 'Annuelle')], verbose_name='Fréquence de la cotisation', null=True, default='ANN', max_length=3),
        ),
    ]
