from django.contrib import admin
from django.db.models.fields import FieldDoesNotExist
from django.template.defaultfilters import slugify
from django.http import HttpResponse


class FieldNotFound(Exception):
    pass


class HeaderDataMixin(admin.ModelAdmin):

    def get_header_data(self, headers):
        '''
        Get the headers verbose name from the header list
        '''
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
        return header_data

    def get_instance_data(self, headers, instance):
        '''
        Get the data corresponding to the header list in the instance
        '''
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
        return data


class CSVExport(HeaderDataMixin, admin.ModelAdmin):
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

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
                                                    slugify(self.model.__name__)
                                                    )
        headers = list(self.list_display)
        writer = csv.DictWriter(response, headers)

        writer.writerow(self.get_header_data(headers))

        # Write records.
        for instance in queryset[:self.csv_record_limit]:
            writer.writerow(self.get_instance_data(headers, instance))
        return response
    csv_export.short_description = 'Exporter la sélection au format CSV'


class LaTeXExport(HeaderDataMixin, admin.ModelAdmin):
        """
        Adds a LaTeX export action to an admin view.
        """

        # This is the maximum number of records that will be written.
        # Exporting massive numbers of records should be done asynchronously.
        tex_record_limit = 1000

        def get_actions(self, request):
            actions = self.actions if hasattr(self, 'actions') else []
            actions.append('tex_export')
            actions = super(LaTeXExport, self).get_actions(request)
            return actions

        def tex_export(self, request, queryset=None, *args, **kwargs):
            from django.template.loader import render_to_string
            response = HttpResponse(content_type='text/tex')
            response['Content-Disposition'] = 'attachment; filename={}.tex'.format(
                                                        slugify(self.model.__name__)
                                                        )
            headers = list(self.list_display)

            context = {}
            context["headers"] = [ head for head in
                                        self.get_header_data(headers).values()]
            context["data"] = []

            for instance in queryset[:self.tex_record_limit]:
                context["data"].append([ head for head in
                            self.get_instance_data(headers, instance).values()]
                            )

            response.write(render_to_string('export/table.tex', context))

            return response
        tex_export.short_description = 'Exporter la sélection au format LaTeX'


class PDFExport(HeaderDataMixin, admin.ModelAdmin):
        """
        Adds a pdf export action to an admin view.
        """

        # This is the maximum number of records that will be written.
        # Exporting massive numbers of records should be done asynchronously.
        pdf_record_limit = 1000

        def get_actions(self, request):
            actions = self.actions if hasattr(self, 'actions') else []
            actions.append('pdf_export')
            actions = super(PDFExport, self).get_actions(request)
            return actions

        def pdf_export(self, request, queryset=None, *args, **kwargs):
            from io import BytesIO
            from reportlab.pdfgen import canvas
            from reportlab.lib import colors, pagesizes, styles
            from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                            Paragraph, Spacer)

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename={}.pdf'.format(
                                                        slugify(self.model.__name__)
                                                        )
            headers = list(self.list_display)

            buff = BytesIO()
            document = SimpleDocTemplate(buff, pagesize=pagesizes.A4)
            elements = []
            styles = styles.getSampleStyleSheet()

            # TODO: Add the filters applied to the view. For example:
            # # Prints the filters applied :
            # p = Paragraph("Filters: ", styles["Normal"])
            # elements.append(p)

            # for key, val in request.GET.items():
            #     p = Paragraph(key+": "+val, styles["Normal"])
            #     elements.append(p)

            # Add some space
            elements.append(Spacer(1, 12))

            table_data = [[ val for val in self.get_header_data(headers).values()]]

            for instance in queryset[:self.pdf_record_limit]:
                table_data += [[ val for val in
                            self.get_instance_data(headers, instance).values()
                              ]]

            alternating_color = [('BACKGROUND', (0,2*n+1), (-1,2*n+1),
                                  colors.lightgrey)
                                 for n in range(len(table_data)//2)]
            table = Table(table_data,
                        style=[('LINEAFTER', (0, 0), (-2, -1), 2, colors.grey),
                               ('LINEBELOW', (0, 0), (-1, 0), 2, colors.grey)
                               ] + alternating_color)
            elements.append(table)
            document.build(elements)

            response.write(buff.getvalue())
            buff.close()
            return response
        pdf_export.short_description = 'Exporter la sélection au format PDF'

class ExportMixin(CSVExport, PDFExport):
    pass
