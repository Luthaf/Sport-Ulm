# -*- coding: utf-8 -*-
from django.db import models

from profilENS.models import User

COTIZ_FREQUENCY_CHOICES = (
    ("SEM", "Semestrielle"),
    ("ANN", "Annuelle")
)


class Sport(models.Model):
    name = models.CharField("Nom", max_length=50)
    price = models.IntegerField(u"Cotisation (€)",
                                blank=True,
                                null=True)
    respo = models.ManyToManyField("Sportif", blank=True, null=True)
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
    user = models.ForeignKey(Sportif, verbose_name="Sportif")
    sport = models.ForeignKey(Sport, verbose_name="Sport")
    payed = models.BooleanField("Payé",
                                default=False)

    class Meta:
        verbose_name = "Sport"

    def __unicode__(self):
        return self.user.__unicode__() + " fait du " + self.sport.__unicode__()


class Event(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nom")
    users = models.ManyToManyField(Sportif,
                                   blank=True,
                                   through='UsersInEvent')
    class Meta:
        verbose_name = "Évènement"

    def __unicode__(self):
        return self.name


class EventOption(models.Model):
    event = models.ForeignKey(Event,
                              verbose_name="Évènement",
                              related_name="prices")
    price = models.IntegerField("Tarif (€)")
    description = models.CharField("Description",
                                   max_length=255)

    class Meta:
        verbose_name = "Prix d'évènement"

    def __unicode__(self):
        return self.description


class UsersInEvent(models.Model):
    user = models.ForeignKey(Sportif, verbose_name="Sportif")
    event = models.ForeignKey(Event, verbose_name="Évènement")
    options = models.ManyToManyField(EventOption, verbose_name="Options")
    payed = models.BooleanField("Payé", default=False)

    class Meta:
        verbose_name = "Participant aux évènements"
        verbose_name_plural = "Participants aux évènements"

    def __unicode__(self):
        return self.user.__unicode__()
