# -*- coding: utf-8 -*-
from django.db import models

COTIZ_FREQUENCY_CHOICES = (
    ("SEM", "Semestrielle"),
    ("ANN", "Annuelle")
)


class Sport(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField("Cotisation",
                                blank=True,
                                null=True)
    respo = models.ManyToManyField("UserBDS")
    cotisation_frequency = models.CharField("Fréquence de la cotisation",
                             default="ANN",
                             choices=COTIZ_FREQUENCY_CHOICES,
                             max_length=3)
    # horaire
    # lieu


class UserBDS(models.Model):
    FFSU_licence = models.BooleanField("Licence FFSU")
    FFSU_number = models.CharField(max_length=50,
                                  blank=True,
                                  null=True)
    certificate = models.BooleanField("Certificat de santé")
    certificate_file = models.BooleanField("Certificat de santé")
    
    sports = models.ManyToManyField(Sport,
                                    blank=True,
                                    through='UsersInSport')
    
    class Meta:
        verbose_name = "Sportif"


class UsersInSport(models.Model):
    user = models.ForeignKey(UserBDS)
    sport = models.ForeignKey(Sport)
    payed = models.BooleanField("Payé")
    
    class Meta:
        verbose_name = "Cotisation"


class Event(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField("Tarif",
                                blank=True,
                                null=True)
    users = models.ManyToManyField(UserBDS,
                                   blank=True,
                                   through='UsersInEvent')
    class Meta:
        verbose_name = "Évènement"
                                           
class UsersInEvent(models.Model):
    user = models.ForeignKey(UserBDS)
    event = models.ForeignKey(Event)
    payed = models.BooleanField("Payé")
    
    class Meta:
        verbose_name = "Participant"