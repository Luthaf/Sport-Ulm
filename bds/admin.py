# -*- coding: utf-8 -*-
from django.contrib import admin

from bds.models import UserBDS, Sport, UsersInSport, Event, UsersInEvent

admin.site.register(UserBDS)
admin.site.register(Sport)
admin.site.register(UsersInSport)
admin.site.register(Event)
admin.site.register(UsersInEvent)