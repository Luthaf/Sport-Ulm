# -*- coding: utf-8 -*-
from django.contrib import admin
from django.core.urlresolvers import reverse

from bds.models import Sportif, Sport, UsersInSport, Event, UsersInEvent, \
                       EventOption, SportTimeSlot, EventTimeSlot
from bds.filters import boolean_filter_factory
from bds.forms import SportifAdminForm, SportAdminForm, SportifInEventAdminForm

from profilENS.models import User, GENDER_CHOICES

from shared.utils import get_model_fields
from shared.export import ExportMixin

def boolean(description=""):
    """
    Convert a admin class method to a boolean widget,
    with short_description=description
    """
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)
        wrapper.boolean = True
        wrapper.short_description = description
        return wrapper
    return decorator

user_fields = get_model_fields(User)


class SportsInline(admin.TabularInline):
    model = Sportif.sports.through
    extra = 0


class SportifAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('user', 'gender', 'have_ffsu', 'is_AS_PSL', 'have_certificate',
                    'phone', 'email', 'departement', 'occupation',
                    'cotisation', 'respo', 'registration_date')
    list_filter = ('have_certificate',
                   boolean_filter_factory('have_ffsu'),
                   boolean_filter_factory("is_AS_PSL"),
                   'user__gender',
                   'registration_date'
                   )

    ordering = ['user__last_name', 'user__first_name']

    inlines = [SportsInline,]
    form = SportifAdminForm

    search_fields = ['^user__first_name', '^user__last_name']

    @boolean(description="n° FFSU")
    def have_ffsu(self, obj):
        return obj.FFSU_number != None and obj.FFSU_number != ""

    def gender(self, obj):
        for (shortGender, gender) in GENDER_CHOICES:
            if shortGender == obj.user.gender:
                return gender
        return 'Inconnu'
    gender.short_description = 'Genre'

    @boolean(description="AS PSL")
    def is_AS_PSL(self, obj):
        return obj.ASPSL_number != None and obj.ASPSL_number != ""

    def respo(self, obj):
        '''Show the sports this sportif is respo'''
        list = ", ".join([sport.name for sport in obj.sports.all() if obj in sport.respo.all()])
        if len (list) == 0:
            list = ""
        return list
    respo.short_description = "Respo"


class SportTimeSlotsInline(admin.TabularInline):
    model = SportTimeSlot
    extra = 1


class SportAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'cotisation_frequency', 'respo_name', "sportifs")
    search_fields = ["^name"]
    form = SportAdminForm
    ordering = ["name"]

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


class UsersInEventAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('user', 'event', 'options_selected', 'payed')
    list_filter = ('event__name', 'payed')
    search_fields = ["^event__name",
                     "^user__user__first_name",
                     "^user__user__last_name"]
    ordering = ["event__name", "user__user__last_name", "user__user__first_name"]

    form = SportifInEventAdminForm

    def options_selected(self, obj):
        options = obj.options.all()
        options_string = []
        total = 0
        for option in options:
            options_string.append(option.description + ' (' + str(option.price) + '€)')
            total += option.price

        options_string.append('Total: ' + str(total) + '€')
        return ','.join(options_string)
    options_selected.short_description = 'Options sélectionnées'


admin.site.register(Sportif, SportifAdmin)
admin.site.register(Sport, SportAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(UsersInEvent, UsersInEventAdmin)
