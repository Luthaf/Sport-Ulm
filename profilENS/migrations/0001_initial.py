# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(max_length=20, verbose_name=b'T\xc3\xa9l\xc3\xa9phone', blank=True)),
                ('occupation', models.CharField(default=b'1A', max_length=3, verbose_name=b'Statut', choices=[(b'EXT', b'Ext\xc3\xa9rieur'), (b'1A', b'1A'), (b'2A', b'2A'), (b'3A', b'3A'), (b'4A', b'4A'), (b'ARC', b'Archicube'), (b'DOC', b'Doctorant'), (b'CST', b'CST')])),
                ('cotisation', models.CharField(default=b'NOR', max_length=3, verbose_name=b'Type de cotisation', choices=[(b'ETU', b'\xc3\x89tudiant'), (b'NOR', b'Normalien'), (b'EXT', b'Ext\xc3\xa9rieur')])),
                ('birthdate', models.DateField(null=True, verbose_name=b'Date de naissance', blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Departement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'D\xc3\xa9partement')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='user',
            name='departement',
            field=models.ForeignKey(blank=True, to='profilENS.Departement', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
            preserve_default=True,
        ),
    ]
