# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '__first__'),
        ('bds', '0002_sportif_cotisation_period'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='description',
            field=models.CharField(blank=True, verbose_name='description', null=True, max_length=255),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.ManyToManyField(verbose_name='Dates et lieux', to='commons.EventPlaceAndTime'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sport',
            name='locations',
            field=models.ManyToManyField(verbose_name='Dates et lieux', to='commons.PlaceAndTime'),
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
            field=models.CharField(blank=True, verbose_name='Numéro AS PSL', null=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='sportif',
            name='FFSU_number',
            field=models.CharField(blank=True, verbose_name='Numéro FFSU', null=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='sportif',
            name='certificate_file',
            field=models.FileField(blank=True, verbose_name='Fichier de certificat médical', upload_to='certifs'),
        ),
        migrations.AlterField(
            model_name='usersinevent',
            name='options',
            field=models.ManyToManyField(blank=True, verbose_name='Options', null=True, to='bds.EventOption'),
        ),
    ]
