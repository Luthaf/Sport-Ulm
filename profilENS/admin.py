# -*- coding: utf-8 -*-
from django.contrib import admin

from profilENS.models import Departement, Clipper, Profile


admin.site.register(Departement)
admin.site.register(Clipper)
admin.site.register(Profile)