# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, CreateView

from profilENS.models import User
from profilENS.forms import UserCreationForm


class UserView(DetailView):
    context_object_name = "showed_user"
    model = User
    template_name = "user/show_user.html"

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.kwargs["username"])


class UserList(ListView):
    model = User
    context_object_name = "user_list"
    template_name = "user/user_list.html"
    paginate_by = 30

    def get_queryset(self):
        return User.objects.all()


class NewUser(CreateView):
    model = User
    template_name = 'user/new_user.html'
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse('user_list')
