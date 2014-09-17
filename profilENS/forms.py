# -*- coding: utf-8 -*-

from django import forms

from profilENS.models import User

class UserCreationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name',
                'last_name',
                'username',
                'email',
                'phone',
                'birthdate',
                'departement',
                'occupation',
                'cotisation')
