from django.db import models


class PlaceMixin(models.Model):
    place = models.CharField("Lieu", max_length=70)
    class Meta:
        abstract = True


class StartTimeMixin(models.Model):
    start_time = models.TimeField("Heure de début")

    class Meta:
        abstract = True


class EndTimeMixin(models.Model):
    end_time = models.TimeField("Heure de fin")

    class Meta:
        abstract = True


class SingleDayMixin(models.Model):
    day = models.CharField("Jour", max_length=15)

    class Meta:
        abstract = True


class StartEventMixin(models.Model):
    start_time = models.DateTimeField("Jour de début")

    class Meta:
        abstract = True


class EndEventMixin(models.Model):
    end_time = models.DateTimeField("Jour de fin")

    class Meta:
        abstract = True

class PlaceAndTime(SingleDayMixin, StartTimeMixin, EndTimeMixin, PlaceMixin):
    pass

class EventPlaceAndTime(StartEventMixin, EndEventMixin, PlaceMixin):
    pass
