# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

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

class Clipper(models.Model):
    username = models.CharField("Identifiant",
                                max_length = 20)
    fullname = models.CharField("Nom complet",
                                max_length = 200)

    def __unicode__(self):
        return unicode(self.username)
    
    class Meta:
        verbose_name = "Profil Clipper"
        verbose_name_plural = "Profils Clipper"
        
        
class Profile(models.Model):
    user = models.OneToOneField(User)
    clipper = models.ForeignKey(Clipper,
                                blank=True,
                                null=True)
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
    
    def __unicode__(self):
        return unicode(self.user.username)
    
    class Meta:
        verbose_name = "Profil ENS"
        verbose_name_plural = "Profils ENS"
    
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
