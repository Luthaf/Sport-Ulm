# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.conf.urls import patterns, url

from profilENS.models import Departement, User
from profilENS.views import AddUserToBuro


class UserAdmin(admin.ModelAdmin):

    actions = ['add_to_buro']
    list_display = ('first_name', 'last_name', 'phone', 'email', 'departement',
                    'occupation', 'cotisation', 'user_group', 'is_staff')
    list_filter = ('occupation', 'cotisation', 'is_staff')

    fieldsets = (
            (None, {
                 'fields': ('first_name',
                            'last_name',
                            'username',
                            'email',
                            'phone',
                            'birthdate')
            }),

            ("ENS", {
                'fields': ('departement', 'occupation', 'cotisation')
            }),
    )
    prepopulated_fields = {'username': ('first_name', 'last_name'), }


    def user_group(self, user):
        '''Show all the groups of the user'''
        return ", ".join([group.name for group in user.groups.all()])
    user_group.short_description = "Burô"

    def add_to_buro(self, request, queryset):
        kwargs = {}
        if len(queryset) != 1:
            import django.contrib.messages as messages
            self.message_user(request,
                              "Un seul utilisateur peut être ajouté à la fois",
                              level=messages.WARNING)
            next_url = "admin:profilENS_user_changelist"
        else:
            next_url = "admin:add_user_to_buro"
            kwargs["pk"] = queryset[0].pk
        return redirect(reverse(next_url, kwargs=kwargs))

    add_to_buro.short_description = "Ajouter l'utilisateur au burô"

    def get_urls(self):
        urls = super(UserAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'(?P<pk>\d+)/add_to_buro$',
            AddUserToBuro.as_view(),
            name="add_user_to_buro"
            ),
        )
        return my_urls + urls


admin.site.register(Departement)
admin.site.register(User, UserAdmin)

admin.site.unregister(Group)
