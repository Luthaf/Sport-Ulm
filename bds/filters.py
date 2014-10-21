# -*- coding: utf-8 -*-
from django.contrib.admin import SimpleListFilter

def boolean_filter_factory(value):
    class BooleanMethodFilter(SimpleListFilter):

        parameter_name = value
        title = ""

        def lookups(self, request, model_admin):
            self.model_admin = model_admin
            self.title = getattr(model_admin, value).short_description
            return (
                (True, 'Oui'),
                (False, 'Non'),
                )

        def queryset(self, request, queryset):
            method = getattr(self.model_admin, value)
            exclude = []
            if self.value() is None:
                return queryset
            for obj in queryset:
                if not(self.value() == str(method(obj))):
                    exclude.append(obj.id)

            return queryset.exclude(id__in=exclude)

    return BooleanMethodFilter
