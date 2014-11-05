from django.http import HttpResponse

def export_as_csv(request, queryset):
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

def export_as_tex(request, queryset):
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


def export_as_pdf(request, queryset):  
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
