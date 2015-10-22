# -*- coding: utf-8 -*-
from django.db import models

from profilENS.models import User
from shared.models import TimeSlot, WeeklyTimeSlot

import os, datetime

COTIZ_FREQUENCY_CHOICES = (
    ("SEM", "semestre"),
    ("ANN", "année"),
    ("COU", "cours")
)


class Sport(models.Model):
    name = models.CharField("Nom", max_length=50)
    price = models.DecimalField("Cotisation (€)",
                                decimal_places=2,
                                max_digits=5,
                                blank=True,
                                null=True)
    respo = models.ManyToManyField("Sportif", blank=True)
    cotisation_frequency = models.CharField("Fréquence de la cotisation",
                                            default="ANN",
                                            choices=COTIZ_FREQUENCY_CHOICES,
                                            max_length=3,
                                            null=True,
                                            blank=True)

    def __str__(self):
        if self.price:
            rep = self.name + ' ( ' + str(self.price) + ' € par ' + str(self.cotisation_frequency)+ ')'
        else:
            rep = self.name
        return rep


class SportTimeSlot(WeeklyTimeSlot):
    sport = models.ForeignKey(Sport)

    class Meta:
        verbose_name = "Crénau"
        verbose_name_plural = "Crénaux"


class Sportif(models.Model):
    def issue_file_name(sportif, filename):
        fn, extension = os.path.splitext(filename)
        year = str(datetime.datetime.now().year)
        return "certifs/" + sportif.__str__() + '-' + year + extension

    COTIZ_DURATION_CHOICES = (
        ('ANN', 'Année'),
        ('SE1', 'Premier semestre'),
        ('SE2', 'Deuxième semestre'),
    )

    user = models.OneToOneField(User, verbose_name="Utilisateur")
    FFSU_number = models.CharField("Numéro FFSU",
                                  max_length=50,
                                  blank=True,
                                  null=True)
    have_certificate = models.BooleanField("Certificat médical",
                                            default=False)
    certificate_file = models.FileField("Fichier de certificat médical",
                                        upload_to=issue_file_name,
                                        blank=True)
    sports = models.ManyToManyField(Sport,
                                    blank=True,
                                    through='UsersInSport')
    ASPSL_number = models.CharField("Numéro AS PSL",
                                    max_length=50,
                                    blank=True,
                                    null=True)
    cotisation_period = models.CharField("Inscription",
                             default="ANN",
                             choices=COTIZ_DURATION_CHOICES,
                             max_length=3)

    registration_date = models.DateField(auto_now_add=True,
                                         auto_now=True,
                                         verbose_name="Date d'inscription")


    class Meta:
        verbose_name = "Sportif"

    def __str__(self):
        return str(self.user)

    @property
    def departement(self):
        return self.user.departement

    @property
    def phone(self):
        return self.user.phone

    @property
    def email(self):
        return self.user.email

    @property
    def occupation(self):
        return self.user.occupation

    @property
    def cotisation(self):
        return self.user.cotisation


class UsersInSport(models.Model):
    user = models.ForeignKey(Sportif, verbose_name="Sportif")
    sport = models.ForeignKey(Sport, verbose_name="Sport")
    payed = models.BooleanField("Payé",
                                default=False)

    class Meta:
        verbose_name = "Sport"

    def __str__(self):
        return str(self.user) + " fait du " + str(self.sport)


class Event(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nom")
    users = models.ManyToManyField(Sportif,
                                   blank=True,
                                   through='UsersInEvent')
    description = models.TextField("description",
                                   null=True,
                                   blank=True)

    class Meta:
        verbose_name = "Évènement"

    def __str__(self):
        return self.name


class EventTimeSlot(TimeSlot):
    event = models.ForeignKey(Event)

    class Meta:
        verbose_name = "Localisation spatio-temporelle"


class EventOption(models.Model):
    event = models.ForeignKey(Event,
                              verbose_name="Évènement",
                              related_name="prices")
    price = models.IntegerField("Tarif (€)")
    description = models.CharField("Description",
                                   max_length=255)

    class Meta:
        verbose_name = "Option"

    def __str__(self):
        return self.description


class UsersInEvent(models.Model):
    user = models.ForeignKey(Sportif, verbose_name="Sportif")
    event = models.ForeignKey(Event, verbose_name="Évènement")
    options = models.ManyToManyField(EventOption,
                                     verbose_name="Options",
                                     blank=True)
    payed = models.BooleanField("Payé", default=False)

    class Meta:
        verbose_name = "Participant aux évènements"
        verbose_name_plural = "Participants aux évènements"

    def __str__(self):
        return str(self.user)
