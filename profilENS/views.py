# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group

from profilENS.models import User
from profilENS.forms import UserCreationForm, AddUserToBuroForm


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


class AddUserToBuro(UpdateView):
    form_class = AddUserToBuroForm
    template_name = "admin/add_to_buro.html"
    success_url = reverse_lazy("admin:profilENS_user_changelist")

    # Change this line if the gestioCOF code is merged with this one
    # to something like (self.request.GET.get("buro", ""))
    buro = "BDS"
    # and don't forget to check for a valid value

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk", -1)
        return get_object_or_404(User, pk=pk)

    def get_context_data(self, *args, **kwargs):
        context = super(AddUserToBuro, self).get_context_data(*args, **kwargs)
        context["buro"] = self.buro
        return context

    def form_valid(self, form):
        new_buro = Group.objects.get(name=self.buro)
        password = form.cleaned_data["password1"]
        self.object.is_staff = True
        self.object.groups.add(new_buro)
        self.object.set_password(password)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
