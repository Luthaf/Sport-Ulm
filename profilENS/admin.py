# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from profilENS.models import Departement, User
from profilENS.forms import UserCreationForm


class UserAdmin(admin.ModelAdmin):
    fieldsets = UserCreationForm.Meta.fieldsets + (
                    ("Permissions", {
                        'fields': ('is_staff', 'is_active',
                                    # 'groups',
                                 )
                    }),
                )
    prepopulated_fields = {'username': ('first_name', 'last_name'), }


admin.site.register(Departement)
admin.site.register(User, UserAdmin)
