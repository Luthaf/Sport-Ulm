# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bds', '0002_sportif_cotisation_period'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventTimeSlot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('place', models.CharField(max_length=70, verbose_name='Lieu')),
                ('start_time', models.DateTimeField(verbose_name='Jour de début')),
                ('end_time', models.DateTimeField(verbose_name='Jour de fin')),
                ('event', models.ForeignKey(to='bds.Event')),
            ],
            options={
                'verbose_name': 'Localisation spatio-temporelle',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SportTimeSlot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('day', models.CharField(choices=[('LU', 'lundi'), ('MA', 'mardi'), ('ME', 'mercredi'), ('JE', 'jeudi'), ('VE', 'vendredi'), ('SA', 'samedi'), ('DI', 'dimanche')], max_length=2, verbose_name='Jour')),
                ('start_time', models.TimeField(verbose_name='Heure de début')),
                ('end_time', models.TimeField(verbose_name='Heure de fin')),
                ('place', models.CharField(max_length=70, verbose_name='Lieu')),
                ('sport', models.ForeignKey(to='bds.Sport')),
            ],
            options={
                'verbose_name_plural': 'Crénaux',
                'verbose_name': 'Crénau',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='description',
            field=models.CharField(verbose_name='description', null=True, max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sportif',
            name='have_certificate',
            field=models.BooleanField(verbose_name='Certificat médical', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sportif',
            name='ASPSL_number',
            field=models.CharField(verbose_name='Numéro AS PSL', null=True, max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='sportif',
            name='FFSU_number',
            field=models.CharField(verbose_name='Numéro FFSU', null=True, max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='sportif',
            name='certificate_file',
            field=models.FileField(upload_to='certifs', verbose_name='Fichier de certificat médical', blank=True),
        ),
        migrations.AlterField(
            model_name='usersinevent',
            name='options',
            field=models.ManyToManyField(verbose_name='Options', null=True, to='bds.EventOption', blank=True),
        ),
    ]
