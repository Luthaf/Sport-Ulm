# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from profilENS.views import UserView, UserList, NewUser, EditUser

urlpatterns = patterns('profilENS.views',
    url(r'^$',
        UserList.as_view(),
        name='user_list'),
    url(r'^new$',
        NewUser.as_view(),
        name='new_user'),
    url(r'^(?P<username>[\w-]+)/$',
        UserView.as_view(),
        name='show_user'),
    url(r'^(?P<username>[\w-]+)/edit$',
        EditUser.as_view(),
        name='edit_user'),
)
