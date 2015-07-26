# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser

OCCUPATION_CHOICES = (
    ('EXT', "Extérieur"),
    ('1A', "1A"),
    ('2A', "2A"),
    ('3A', "3A"),
    ('4A', "4A"),
    ('MAG', "Magistérien"),
    ('ARC', "Archicube"),
    ('DOC', "Doctorant"),
    ('CST', "CST"),
    ('PER', "Personnel ENS"),
)

TYPE_COTIZ_CHOICES = (
    ('ETU', "Étudiant"),
    ('NOR', "Normalien"),
    ('EXT', "Extérieur"),
    ('ARC', "Archicube"),
)

GENDER_CHOICES = (
    ('MAL', "Homme"),
    ('FEM', "Femme"),
    ('OTH', "Autre")
)


class Departement(models.Model):
    name = models.CharField("Département",
                            max_length = 50)

    def __str__(self):
        return self.name


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
    gender = models.CharField("Sexe",
                              choices=GENDER_CHOICES,
                              max_length=3)

    def __str__(self):
        if self.first_name and self.last_name:
            u = self.first_name + " " + self.last_name
        elif self.first_name:
            u = self.first_name
        elif self.last_name:
            u = self.last_name
        else:
            u = self.username
        return u

    #TODO: Add a password change view
