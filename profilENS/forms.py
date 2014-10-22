from django import forms

from profilENS.models import User

class AddUserToBuroForm(forms.ModelForm):
    password1 = forms.CharField(label="Le mot magique",
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label="Encore une fois",
                                widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return password2

    class Meta:
        model = User
        fields = tuple()
