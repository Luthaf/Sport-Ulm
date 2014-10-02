# -*- coding: utf-8 -*-
from django.db import models

from profilENS.models import User

COTIZ_FREQUENCY_CHOICES = (
    ("SEM", "Semestrielle"),
    ("ANN", "Annuelle")
)


class Sport(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField("Cotisation",
                                blank=True,
                                null=True)
    respo = models.ManyToManyField("Sportif")
    cotisation_frequency = models.CharField("Fréquence de la cotisation",
                             default="ANN",
                             choices=COTIZ_FREQUENCY_CHOICES,
                             max_length=3)

    def __unicode__(self):
        return self.name


class Sportif(models.Model):
    user = models.OneToOneField(User, verbose_name="Utilisateur")
    FFSU_number = models.CharField(max_length=50,
                                  blank=True,
                                  null=True)
    certificate_file = models.FileField("Certificat",
                                        upload_to='certifs',
                                        blank=True)

    sports = models.ManyToManyField(Sport,
                                    blank=True,
                                    through='UsersInSport')

    class Meta:
        verbose_name = "Sportif"

    def __unicode__(self):
        return self.user.__unicode__()


class UsersInSport(models.Model):
    user = models.ForeignKey(Sportif)
    sport = models.ForeignKey(Sport)
    payed = models.BooleanField("Payé",
                                default=False)

    class Meta:
        verbose_name = "Lien utilisateurs-sports"
        verbose_name_plural = "Liens utilisateurs-sports"

    def __unicode__(self):
        return self.user.__unicode__() + "fait du" + self.sport.__unicode__()


class Event(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField("Tarif",
                                blank=True,
                                null=True)
    users = models.ManyToManyField(Sportif,
                                   blank=True,
                                   through='UsersInEvent')
    class Meta:
        verbose_name = "Évènement"

    def __unicode__(self):
        return self.name


class UsersInEvent(models.Model):
    user = models.ForeignKey(Sportif)
    event = models.ForeignKey(Event)
    payed = models.BooleanField("Payé",
                                default=False)

    class Meta:
        verbose_name = "Participant aux évènements"
        verbose_name_plural = "Participants aux évènements"

    def __unicode__(self):
        return self.user
