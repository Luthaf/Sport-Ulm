# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include("shared.urls")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^selectable/', include('selectable.urls')),
)

# Serving static files in dev
if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )


# Run the init functions for each installed app
# This allow to define default instances for some models
from django.conf import settings

for app in settings.INSTALLED_APPS:
    try:
        A = __import__(app)
    except ImportError:
        pass

    try:
        A.init()
    except AttributeError:
        pass
