from django import forms
from django.contrib.auth import authenticate

from .models import CardUser


class PinForm(forms.Form):
    number = forms.CharField(max_length=16,
                             min_length=16,
                             widget=forms.HiddenInput())
    password = forms.CharField(max_length=4,
                               min_length=4,
                               widget=forms.PasswordInput())

    def clean(self):
        data = super(PinForm, self).clean()
        user = authenticate(**self.cleaned_data)
        if user:
            self.user = user
        else:
            raise forms.ValidationError("Wrong pin code")
        return data


class LoginForm(forms.Form):
    number = forms.CharField(max_length=16, min_length=16)

    def clean(self):
        data = super(LoginForm, self).clean()
        try:
            user = CardUser.objects.get(number=self.cleaned_data['number'])
        except CardUser.DoesNotExist:
            raise forms.ValidationError("Such card does not exist")
        # TODO: Validate if user is blocked
        user
        return data
