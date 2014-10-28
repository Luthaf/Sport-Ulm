# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='Nom')),
                ('description', models.CharField(max_length=255, verbose_name='description', null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Évènement',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('price', models.IntegerField(verbose_name='Tarif (€)')),
                ('description', models.CharField(max_length=255, verbose_name='Description')),
                ('event', models.ForeignKey(verbose_name='Évènement', to='bds.Event', related_name='prices')),
            ],
            options={
                'verbose_name': 'Option',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventTimeSlot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
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
            name='Sport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='Nom')),
                ('price', models.IntegerField(null=True, verbose_name='Cotisation (€)', blank=True)),
                ('cotisation_frequency', models.CharField(max_length=3, verbose_name='Fréquence de la cotisation', null=True, choices=[('SEM', 'Semestrielle'), ('ANN', 'Annuelle')], default='ANN', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sportif',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('FFSU_number', models.CharField(max_length=50, verbose_name='Numéro FFSU', null=True, blank=True)),
                ('have_certificate', models.BooleanField(verbose_name='Certificat médical', default=False)),
                ('certificate_file', models.FileField(verbose_name='Fichier de certificat médical', upload_to='certifs', blank=True)),
                ('ASPSL_number', models.CharField(max_length=50, verbose_name='Numéro AS PSL', null=True, blank=True)),
                ('cotisation_period', models.CharField(max_length=3, verbose_name='Inscription', choices=[('ANN', 'Année'), ('SE1', 'Premier semestre'), ('SE2', 'Deuxième semestre')], default='ANN')),
            ],
            options={
                'verbose_name': 'Sportif',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SportTimeSlot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('day', models.CharField(max_length=2, verbose_name='Jour', choices=[('LU', 'lundi'), ('MA', 'mardi'), ('ME', 'mercredi'), ('JE', 'jeudi'), ('VE', 'vendredi'), ('SA', 'samedi'), ('DI', 'dimanche')])),
                ('start_time', models.TimeField(verbose_name='Heure de début')),
                ('end_time', models.TimeField(verbose_name='Heure de fin')),
                ('place', models.CharField(max_length=70, verbose_name='Lieu')),
                ('sport', models.ForeignKey(to='bds.Sport')),
            ],
            options={
                'verbose_name': 'Crénau',
                'verbose_name_plural': 'Crénaux',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsersInEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('payed', models.BooleanField(verbose_name='Payé', default=False)),
                ('event', models.ForeignKey(verbose_name='Évènement', to='bds.Event')),
                ('options', models.ManyToManyField(null=True, verbose_name='Options', to='bds.EventOption', blank=True)),
                ('user', models.ForeignKey(verbose_name='Sportif', to='bds.Sportif')),
            ],
            options={
                'verbose_name': 'Participant aux évènements',
                'verbose_name_plural': 'Participants aux évènements',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsersInSport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('payed', models.BooleanField(verbose_name='Payé', default=False)),
                ('sport', models.ForeignKey(verbose_name='Sport', to='bds.Sport')),
                ('user', models.ForeignKey(verbose_name='Sportif', to='bds.Sportif')),
            ],
            options={
                'verbose_name': 'Sport',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sportif',
            name='sports',
            field=models.ManyToManyField(through='bds.UsersInSport', to='bds.Sport', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sportif',
            name='user',
            field=models.OneToOneField(verbose_name='Utilisateur', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sport',
            name='respo',
            field=models.ManyToManyField(null=True, to='bds.Sportif', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='users',
            field=models.ManyToManyField(through='bds.UsersInEvent', to='bds.Sportif', blank=True),
            preserve_default=True,
        ),
    ]
