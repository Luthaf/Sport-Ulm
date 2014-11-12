# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic import UpdateView
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.http import HttpResponse

from profilENS.models import User
from profilENS.forms import AddUserToBuroForm
from profilENS.sync import sync_with_clipper

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

def update_from_clipper(request):
    ''' Call the sync script and return to the previous page.'''

    sync_with_clipper()
    message = "Yeah!"

    return HttpResponse(message)

def update_from_clipper_status(request):
    ''' Ask the database about the status of the update '''
    import redis
    r = redis.StrictRedis()
    message_ssh = " Récupération de la liste des utilisateurs depuis clipper…"
    message_db = " Récupération des données de la base de donnée… "
    message_sync = "Mise à jour de la base de donnée…"

    try:
        status = r.get("status").decode()
        if status == "ssh":
            message = message_ssh
        elif status == "db":
            message = message_db
        elif status == "sync":
            n_tot_user = int(r.get("n_total_user"))
            n_user = int(r.get("n_user"))
            message = message_sync + "[{}/{}]".format(n_user, n_tot_user)
    except AttributeError:
        message= ""
    return HttpResponse(message)

