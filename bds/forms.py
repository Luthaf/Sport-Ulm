# -*- coding: utf-8 -*-
from django import forms
from selectable.forms.widgets import (AutoCompleteSelectWidget,
            AutoCompleteSelectMultipleWidget)

from bds.models import Sportif, Sport, UsersInEvent
from bds.lookups import SportifLookup, EventLookup
from profilENS.lookups import UserLookup


class SportifAdminForm(forms.ModelForm):

    class Meta(object):
        model = Sportif
        widgets = {
            'user': AutoCompleteSelectWidget(lookup_class=UserLookup),
        }
        exclude = tuple()


class SportAdminForm(forms.ModelForm):

    class Meta(object):
        model = Sport
        widgets = {
          'respo': AutoCompleteSelectMultipleWidget(lookup_class=SportifLookup),
        }
        exclude = tuple()


class SportifInEventAdminForm(forms.ModelForm):

    class Meta(object):
        model = UsersInEvent
        widgets = {
          'user': AutoCompleteSelectWidget(lookup_class=SportifLookup),
          'event': AutoCompleteSelectWidget(lookup_class=EventLookup),
        }
        exclude = tuple()
