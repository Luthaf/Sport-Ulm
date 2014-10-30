# -*- coding: utf-8 -*-
from django.contrib import admin
from django.core.urlresolvers import reverse

from bds.models import Sportif, Sport, UsersInSport, Event, UsersInEvent, \
                       EventOption, SportTimeSlot, EventTimeSlot
from bds.filters import boolean_filter_factory
from bds.forms import SportifAdminForm, SportAdminForm, SportifInEventAdminForm

from profilENS.models import User


def boolean(description=""):
    """
    Convert a admin class method to a boolean widget,
    with short_description=description
    """
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)
        wrapper.boolean=True
        wrapper.short_description = description
        return wrapper
    return decorator

def get_model_fields(model):
    fields = {}
    options = model._meta
    for field in sorted(options.concrete_fields + \
                        options.many_to_many + \
                        options.virtual_fields):
        fields[field.name] = field
    return fields

user_fields = get_model_fields(User)


class SportsInline(admin.TabularInline):
    model = Sportif.sports.through
    extra = 0


class SportifAdmin(admin.ModelAdmin):
    list_display = ('user', 'have_ffsu', 'is_AS_PSL', 'have_certificate',
                    'phone', 'email', 'departement', 'occupation',
                    'cotisation', 'respo')
    list_filter = ('have_certificate',
                   boolean_filter_factory('have_ffsu'),
                   boolean_filter_factory("is_AS_PSL"),
                   )

    inlines = [SportsInline,]
    form = SportifAdminForm

    search_fields = ['^user__first_name', '^user__last_name']

    @boolean(description="n° FFSU")
    def have_ffsu(self, obj):
        return obj.FFSU_number != None and obj.FFSU_number != ""

    @boolean(description="AS PSL")
    def is_AS_PSL(self, obj):
        return obj.ASPSL_number != None and obj.ASPSL_number != ""

    def respo(self, obj):
        '''Show the sports this sportif is respo'''
        return ", ".join([sport.name for sport in obj.sports.all() if obj in sport.respo.all()])
    respo.short_description = "Respo"


class SportTimeSlotsInline(admin.TabularInline):
    model = SportTimeSlot
    extra = 1


class SportAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'cotisation_frequency', 'respo_name', "sportifs")
    search_fields = ["^name"]
    form = SportAdminForm

    inlines = [SportTimeSlotsInline, ]
    exclude = ['time_slots']


    def respo_name(self, obj):
        respos = obj.respo.all()
        respos_urls = []
        for respo in respos:
            url = reverse("admin:bds_sportif_change", args=(respo.id,))
            respos_urls.append('<a href="' + url + '">' + str(respo) + "</a>")
        return "\n".join(respos_urls)
    respo_name.short_description = "Respo(s)"
    respo_name.allow_tags = True

    def sportifs(self, obj):
        return obj.sportif_set.count()


class EventOptionInline(admin.TabularInline):
    model = EventOption
    extra = 0


class EventTimeSlotsInline(admin.TabularInline):
    model = EventTimeSlot
    extra = 1
    max_num = 1


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'participants')
    search_fields = ["^name"]
    inlines = [EventOptionInline, EventTimeSlotsInline]

    def participants(self, obj):
        return obj.users.all().count()


class UsersInEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'payed')
    list_filter = ('event__name', 'payed')
    search_fields = ["^event__name",
                     "^user__user__first_name",
                     "^user__user__last_name"]

    form = SportifInEventAdminForm


admin.site.register(Sportif, SportifAdmin)
admin.site.register(Sport, SportAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(UsersInEvent, UsersInEventAdmin)
