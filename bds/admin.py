# -*- coding: utf-8 -*-
from django.contrib import admin

from django.db import models

from commons.admin.reverse import ReverseModelAdmin

from bds.models import Sportif, Sport, UsersInSport, Event, UsersInEvent

from profilENS.forms import UserCreationForm


class SportifAdmin(ReverseModelAdmin):
    inline_type = 'stacked'
    inline_reverse = (('user', UserCreationForm), )


admin.site.register(Sportif, SportifAdmin)
admin.site.register(Sport)
admin.site.register(UsersInSport)
admin.site.register(Event)
admin.site.register(UsersInEvent)
