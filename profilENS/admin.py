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

    actions = ['add_to_buro', 'export_as_csv', 'export_as_pdf', 'export_as_tex']
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
        response['Content-Disposition'] = 'attachment; filename="report.csv"'
        
        writer = csv.writer(response, dialect="excel")
        # TODO: get the header dynamically
        writer.writerow(["Utilisateur", "Téléphone", "Occupation",
                         "Département", "Cotisation",
                         "Date de naissance"])
        for user in users:
            writer.writerow([user, user.phone, user.occupation,
                             user.departement, user.cotisation,
                             user.birthdate])
        
        return response
    
    export_as_csv.short_description = "Exporter la selection au format csv"
    
    def export_as_tex(self, request, queryset):
        ''' Export all the columns as tex'''
        # TODO: what to do if array too long ?
        users = queryset
        response = HttpResponse(content_type='text/tex')
        response['Content-Disposition'] = 'attachment; filename="report.tex"'
        
        from io import StringIO
        buffer = StringIO()
        buffer.write("\\documentclass{report}\n\n")
        buffer.write("\\usepackage[utf8]{inputenc}\n\\usepackage[T1]{fontenc}\n")
        buffer.write("\\begin{document}\n")
        buffer.write("\\begin{tabular}{l|l|l|l|l|l}\n\t\n")
        sep = " & "
        buffer.write("\t"+sep.join(["Utilisateur", "Téléphone", "Occupation",
                                    "Département", "Cotisation",
                                    "Date de naissance"]) + "\\\\\\hline\n")
        buffer.write("\t"+
                     "\\\\\n\t".join(
                         [sep.join([str(user), str(user.phone),
                                    str(user.occupation), str(user.departement),
                                    str(user.cotisation),str(user.birthdate)])
                          for user in users])
                     + "\n")
        buffer.write("\\end{tabular}\n")
        buffer.write("\\end{document}")        
        response.write(buffer.getvalue())

        return response
    
    export_as_tex.short_description = "Exporter la selection au format tex"

      
    def export_as_pdf(self, request, queryset):  
        """Returns PDF as a binary stream."""
        # TODO: count number of pages
        # TODO: add user id
        from io import BytesIO
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
        from reportlab.platypus import Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles=getSampleStyleSheet()

        # TODO: Add the filters applied to the view. For example:
        # # Prints the filters applied :
        # p = Paragraph("Filters: ", styles["Normal"])
        # elements.append(p)

        # for key, val in request.GET.items():
        #     p = Paragraph(key+": "+val, styles["Normal"])
        #     elements.append(p)

        # Add some space
        elements.append(Spacer(1, 12))
        
        # TODO: get the header dynamically
        data = [["Utilisateur", "Téléphone", "Occupation",
                         "Département", "Cotisation",
                         "Date de naissance"]]
        data += [ [user, user.phone, user.occupation,
                   user.departement, user.cotisation,
                   user.birthdate] for user in queryset ]
        alternating_color = [('BACKGROUND', (0,2*n+1), (-1,2*n+1),
                              colors.lightgrey)
                             for n in range(len(data)//2)]
        t = Table(data, style=[('LINEAFTER', (0,0), (-2, -1), 2, colors.grey),
                               ('LINEBELOW', (0,0), (-1, 0), 2, colors.grey)]
                  +alternating_color)
        elements.append(t)
        doc.build(elements)
        response.write(buffer.getvalue())
        buffer.close()
        return response
    
    export_as_pdf.short_description = "Exporter la selection au format pdf"

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

