# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from profilENS.views import ProfileView, ProfileList

urlpatterns = patterns('profilENS.views',
    url(r'^$',
        ProfileList.as_view(),
        name='profile_list'),
    url(r'^(?P<username>[\w-]+)/$',
        ProfileView.as_view(),
        name='show_profile'),
)
