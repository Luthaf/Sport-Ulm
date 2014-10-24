# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('shared.views',
    url(r'^$', 'home', name='home'),
)
