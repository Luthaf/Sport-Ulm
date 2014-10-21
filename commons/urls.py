# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('commons.views',
    url(r'^$', 'home', name='home'),
)
