# -*- coding: utf-8 -*-
from django.contrib import admin
from django.core.urlresolvers import reverse

from bds.models import Sportif, Sport, UsersInSport, Event, UsersInEvent, \
                       EventOption
from bds.filters import boolean_filter_factory
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
    list_filter = (boolean_filter_factory('have_certificate'),
                   boolean_filter_factory('have_ffsu'),
                   boolean_filter_factory("is_AS_PSL"),
                   )

    inlines = [SportsInline,]

    for attr in ['phone', 'email', 'departement', 'occupation', 'cotisation']:
        locals()[attr] = lambda self, obj, attr=attr : getattr(obj.user, attr)
        attr_field = user_fields[attr]
        try:
            locals()[attr].short_description = attr_field.verbose_name
        except AttributeError:
            locals()[attr].short_description = attr

    @boolean(description="n° FFSU")
    def have_ffsu(self, obj):
        return obj.FFSU_number != ""

    @boolean(description="AS PSL")
    def is_AS_PSL(self, obj):
        return obj.ASPSL_number != ""

    @boolean(description="Certificat")
    def have_certificate(self, obj):
        return obj.certificate_file != ""

    def respo(self, obj):
        '''Show the sports this sportif is respo'''
        return ", ".join([sport.name for sport in obj.sports.all() if obj in sport.respo.all()])
    respo.short_description = "Respo"


class SportAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'respo_name', 'cotisation_frequency')

    def respo_name(self, obj):
        respos = obj.respo.all()
        respos_urls = []
        for respo in respos:
            url = reverse("admin:bds_sportif_change", args=(respo.id,))
            respos_urls.append('<a href="' + url + '">' + str(respo) + "</a>")
        return "\n".join(respos_urls)
    respo_name.short_description = "Respo(s)"
    respo_name.allow_tags = True


class EventOptionInline(admin.TabularInline):
    model = EventOption
    extra = 1


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'participants')
    inlines = [EventOptionInline]

    def participants(self, obj):
        return obj.users.all().count()


class UsersInEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'payed')
    list_filter = ('event', 'payed')

    #formfield_overrides = {
    #        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    #    }


admin.site.register(Sportif, SportifAdmin)
admin.site.register(Sport, SportAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(UsersInEvent, UsersInEventAdmin)
