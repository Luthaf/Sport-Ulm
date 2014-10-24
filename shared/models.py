from django.db import models

DAY_CHOICES = (
    ("LU", "lundi"),
    ("MA", "mardi"),
    ("ME", "mercredi"),
    ("JE", "jeudi"),
    ("VE", "vendredi"),
    ("SA", "samedi"),
    ("DI", "dimanche"),
)


class WeeklyTimeSlot(models.Model):
    day = models.CharField("Jour", choices=DAY_CHOICES, max_length=2)
    start_time = models.TimeField("Heure de début")
    end_time = models.TimeField("Heure de fin")
    place = models.CharField("Lieu", max_length=70)

    class Meta:
        abstract = True


class TimeSlot(models.Model):
    place = models.CharField("Lieu", max_length=70)
    start_time = models.DateTimeField("Jour de début")
    end_time = models.DateTimeField("Jour de fin")

    class Meta:
        abstract = True
