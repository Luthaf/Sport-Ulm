from django.contrib import admin

from django.db.models.fields import FieldDoesNotExist


class FieldNotFound(Exception):
    pass


class CSVExport(admin.ModelAdmin):
    """
    Adds a CSV export action to an admin view.
    """

    # This is the maximum number of records that will be written.
    # Exporting massive numbers of records should be done asynchronously.
    csv_record_limit = 1000

    def get_actions(self, request):
        actions = self.actions if hasattr(self, 'actions') else []
        actions.append('csv_export')
        actions = super(CSVExport, self).get_actions(request)
        return actions

    def csv_export(self, request, queryset=None, *args, **kwargs):
        import csv
        from django.http import HttpResponse
        from django.template.defaultfilters import slugify

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
                                                    slugify(self.model.__name__)
                                                    )
        headers = list(self.list_display)
        writer = csv.DictWriter(response, headers)

        # Write header.
        header_data = {}
        for name in headers:
            if hasattr(self, name) \
            and hasattr(getattr(self, name), 'short_description'):
                header_data[name] = getattr(
                    getattr(self, name), 'short_description')
            else:
                field = None
                try:
                    field = self.model._meta.get_field_by_name(name)
                except FieldDoesNotExist:
                    field = getattr(self.model, name)

                # This is the case for normal fields, but not properties
                # or OneToOne.
                if isinstance(field, tuple):
                    field = field[0]

                if field and hasattr(field, 'verbose_name'):
                    header_data[name] = field.verbose_name
                else:
                    header_data[name] = name
            header_data[name] = header_data[name].title()
        writer.writerow(header_data)

        # Write records.
        for instance in queryset[:self.csv_record_limit]:
            data = {}
            for name in headers:
                if hasattr(instance, name):
                    data[name] = getattr(instance, name)
                elif hasattr(self, name):
                    data[name] = getattr(self, name)(instance)
                else:
                    raise FieldNotFound('Unknown field: {}'.format(name))

                if callable(data[name]):
                    data[name] = data[name]()
            writer.writerow(data)
        return response
    csv_export.short_description = 'Exporter la sélection au format CSV'


def export_as_tex(modeladmin, request, queryset):
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
export_as_tex.short_description = "Exporter la selection au format LaTeX"

def export_as_pdf(modeladmin, request, queryset):
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
export_as_pdf.short_description = "Exporter la selection au format PDF"
