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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='Nom', max_length=50)),
            ],
            options={
                'verbose_name': 'Évènement',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('price', models.IntegerField(verbose_name='Tarif (€)')),
                ('description', models.CharField(verbose_name='Description', max_length=255)),
                ('event', models.ForeignKey(verbose_name='Évènement', related_name='prices', to='bds.Event')),
            ],
            options={
                'verbose_name': "Prix d'évènement",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='Nom', max_length=50)),
                ('price', models.IntegerField(null=True, verbose_name='Cotisation (€)', blank=True)),
                ('cotisation_frequency', models.CharField(verbose_name='Fréquence de la cotisation', max_length=3, choices=[('SEM', 'Semestrielle'), ('ANN', 'Annuelle')], default='ANN')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sportif',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('FFSU_number', models.CharField(null=True, max_length=50, blank=True)),
                ('certificate_file', models.FileField(verbose_name='Certificat médical', blank=True, upload_to='certifs')),
                ('ASPSL_number', models.CharField(null=True, max_length=50, blank=True)),
            ],
            options={
                'verbose_name': 'Sportif',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsersInEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('payed', models.BooleanField(verbose_name='Payé', default=False)),
                ('event', models.ForeignKey(verbose_name='Évènement', to='bds.Event')),
                ('options', models.ManyToManyField(verbose_name='Options', to='bds.EventOption')),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
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
            field=models.ManyToManyField(to='bds.Sport', blank=True, through='bds.UsersInSport'),
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
            field=models.ManyToManyField(to='bds.Sportif', blank=True, through='bds.UsersInEvent'),
            preserve_default=True,
        ),
    ]
