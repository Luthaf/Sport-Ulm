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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'Nom')),
            ],
            options={
                'verbose_name': '\xc9v\xe8nement',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.IntegerField(verbose_name=b'Tarif (\xe2\x82\xac)')),
                ('description', models.CharField(max_length=255, verbose_name=b'Description')),
                ('event', models.ForeignKey(related_name=b'prices', verbose_name=b'\xc3\x89v\xc3\xa8nement', to='bds.Event')),
            ],
            options={
                'verbose_name': "Prix d'\xe9v\xe8nement",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'Nom')),
                ('price', models.IntegerField(null=True, verbose_name='Cotisation (\u20ac)', blank=True)),
                ('cotisation_frequency', models.CharField(default=b'ANN', max_length=3, verbose_name=b'Fr\xc3\xa9quence de la cotisation', choices=[(b'SEM', b'Semestrielle'), (b'ANN', b'Annuelle')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sportif',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('FFSU_number', models.CharField(max_length=50, null=True, blank=True)),
                ('certificate_file', models.FileField(upload_to=b'certifs', verbose_name=b'Certificat m\xc3\xa9dical', blank=True)),
                ('ASPSL_number', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Sportif',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsersInEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payed', models.BooleanField(default=False, verbose_name=b'Pay\xc3\xa9')),
                ('event', models.ForeignKey(verbose_name=b'\xc3\x89v\xc3\xa8nement', to='bds.Event')),
                ('options', models.ManyToManyField(to='bds.EventOption', verbose_name=b'Options')),
                ('user', models.ForeignKey(verbose_name=b'Sportif', to='bds.Sportif')),
            ],
            options={
                'verbose_name': 'Participant aux \xe9v\xe8nements',
                'verbose_name_plural': 'Participants aux \xe9v\xe8nements',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsersInSport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payed', models.BooleanField(default=False, verbose_name=b'Pay\xc3\xa9')),
                ('sport', models.ForeignKey(verbose_name=b'Sport', to='bds.Sport')),
                ('user', models.ForeignKey(verbose_name=b'Sportif', to='bds.Sportif')),
            ],
            options={
                'verbose_name': 'Sport',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sportif',
            name='sports',
            field=models.ManyToManyField(to='bds.Sport', through='bds.UsersInSport', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sportif',
            name='user',
            field=models.OneToOneField(verbose_name=b'Utilisateur', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sport',
            name='respo',
            field=models.ManyToManyField(to='bds.Sportif', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='users',
            field=models.ManyToManyField(to='bds.Sportif', through='bds.UsersInEvent', blank=True),
            preserve_default=True,
        ),
    ]
