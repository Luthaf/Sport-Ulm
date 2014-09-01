# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('bds.urls')),
    url(r'^profile/', include('profilENS.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
