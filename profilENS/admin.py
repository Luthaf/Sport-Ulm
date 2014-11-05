# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.conf.urls import patterns, url
from django.db import models
from django.http import HttpResponse

from selectable.forms.widgets import AutoCompleteSelectWidget

from profilENS.lookups import DepartementLookup
from profilENS.models import Departement, User
from profilENS.views import AddUserToBuro

class UserAdmin(admin.ModelAdmin):

    actions = ['add_to_buro', 'export_as_csv', 'export_as_pdf']
    list_display = ('user', 'phone', 'email', 'departement',
                    'occupation', 'cotisation', 'user_group', 'is_staff')
    list_filter = ('occupation', 'cotisation', 'departement', 'is_staff')

    search_fields = ['^first_name', '^last_name']
    ordering = ['last_name', 'first_name']

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

    formfield_overrides = {
        models.ForeignKey:
            {'widget': AutoCompleteSelectWidget(lookup_class=DepartementLookup)}
    }

    prepopulated_fields = {'username': ('first_name', 'last_name'), }


    def user_group(self, user):
        '''Show all the groups of the user'''
        return ", ".join([group.name for group in user.groups.all()])
    user_group.short_description = "Burô"

    def user(self, obj):
        return obj.__str__()
    user.short_description = "Utilisateur"

    def add_to_buro(self, request, queryset):
        kwargs = {}
        # FIXME: il faut vérifier len(queryset) > 1 non ?
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

    def export_as_csv(self, request, queryset):
        ''' Export all the columns as CSV'''
        
        import csv
        users = queryset
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="file.csv"'
        
        writer = csv.writer(response, dialect="excel")
        # TODO: get the header dynamically
        writer.writerow(["Utilisateur", "Téléphone", "Occupation",
                         "Déparement", "Cotisation",
                         "Date de naissance"])
        for user in users:
            writer.writerow([user, user.phone, user.occupation,
                             user.departement, user.cotisation,
                             user.birthdate])
        
        return response
    
    export_as_csv.short_description = "Exporter la selection au format csv"

      
    def export_as_pdf(self, request, queryset):  
        """Returns PDF as a binary stream."""
        from io import BytesIO
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="file.pdf"'
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        data = [ [user, user.phone, user.occupation,
                             user.departement, user.cotisation,
                             user.birthdate] for user in queryset ]
        t=Table(data)      
        elements.append(t)
        doc.build(elements)
        response.write(buffer.getvalue())
        buffer.close()
        return response

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

