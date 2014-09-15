# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from profilENS.views import UserView, UserList, NewUser

urlpatterns = patterns('profilENS.views',
    url(r'^$',
        UserList.as_view(),
        name='user_list'),
    url(r'^new/$',
        NewUser.as_view(),
        name='new_user'),
    url(r'^show/(?P<username>[\w-]+)/$',
        UserView.as_view(),
        name='show_user'),
)
