# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser

OCCUPATION_CHOICES = (
    ('EXT', "Extérieur"),
    ('1A', "1A"),
    ('2A', "2A"),
    ('3A', "3A"),
    ('4A', "4A"),
    ('ARC', "Archicube"),
    ('DOC', "Doctorant"),
    ('CST', "CST"),
)

TYPE_COTIZ_CHOICES = (
    ('ETU', "Étudiant"),
    ('NOR', "Normalien"),
    ('EXT', "Extérieur"),
)


class Departement(models.Model):
    name = models.CharField("Département",
                            max_length = 50)

    def __unicode__(self):
        return unicode(self.name)


class User(AbstractUser):
    phone = models.CharField("Téléphone",
                             max_length=20,
                             blank=True)
    occupation = models.CharField("Statut",
                             default="1A",
                             choices=OCCUPATION_CHOICES,
                             max_length=3)
    departement = models.ForeignKey(Departement,
                                    blank=True,
                                    null=True)
    cotisation = models.CharField("Type de cotisation",
                             default="NOR",
                             choices=TYPE_COTIZ_CHOICES,
                             max_length=3)
    birthdate = models.DateField(auto_now_add=False,
                                 auto_now=False,
                                 verbose_name="Date de naissance",
                                 blank=True,
                                 null=True)

    #TODO: Add a password change view
