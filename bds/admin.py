# -*- coding: utf-8 -*-
from django.contrib import admin

from bds.models import Sportif, Sport, UsersInSport, Event, UsersInEvent
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


class SportifAdmin(admin.ModelAdmin):
    list_display = ('user', 'have_ffsu', 'have_certificate', 'phone', 'email', 'departement',
                    'occupation', 'cotisation')

    # TODO: check at https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter
    # http://stackoverflow.com/a/1294952
    #list_filter = ('have_ffsu', 'have_certificate')

    for attr in ['phone', 'email', 'departement', 'occupation', 'cotisation']:
        locals()[attr] = lambda self, obj, attr=attr : getattr(obj.user, attr)
        attr_field = user_fields[attr]
        try:
            locals()[attr].short_description = attr_field.verbose_name
        except AttributeError:
            locals()[attr].short_description = attr

    @boolean(description="FFSU")
    def have_ffsu(self, obj):
        return obj.FFSU_number != ""

    @boolean(description="Certificat")
    def have_certificate(self, obj):
        return obj.certificate_file != ""


admin.site.register(Sportif, SportifAdmin)
admin.site.register(Sport)
admin.site.register(UsersInSport)
admin.site.register(Event)
admin.site.register(UsersInEvent)
