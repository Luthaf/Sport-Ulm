# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from profilENS.models import Profile

class ProfileView(DetailView):
    context_object_name = "user"
    model = Profile
    template_name = "profile/show_profile.html"

    def get_queryset(self):
        return Profile.objects.get(
                        user__username=self.kwargs['username'])


class ProfileList(ListView):
    model = Profile
    context_object_name = "profile_list"
    template_name = "profile/profile_list.html"
    paginate_by = 30

    def get_queryset(self):
        return Profile.objects.all()
