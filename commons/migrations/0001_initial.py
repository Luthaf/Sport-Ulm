# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EventPlaceAndTime',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('place', models.CharField(verbose_name='Lieu', max_length=70)),
                ('start_time', models.DateTimeField(verbose_name='Jour de début')),
                ('end_time', models.DateTimeField(verbose_name='Jour de fin')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlaceAndTime',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('place', models.CharField(verbose_name='Lieu', max_length=70)),
                ('start_time', models.TimeField(verbose_name='Heure de début')),
                ('end_time', models.TimeField(verbose_name='Heure de fin')),
                ('day', models.CharField(verbose_name='Jour', max_length=15)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
