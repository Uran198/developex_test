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
            user.wrong_tries = 0
            user.save()
        else:
            # increment number of wrong tries
            try:
                user = CardUser.objects.get(number=self.cleaned_data['number'])
                user.wrong_tries += 1
                if user.wrong_tries >= 4:
                    user.is_blocked = True
                user.save()
            except CardUser.DoesNotExist:
                pass
            raise forms.ValidationError("Wrong pin code")
        if user.is_blocked:
            raise forms.ValidationError("The card is blocked")
        return data


class LoginForm(forms.Form):
    number = forms.CharField(max_length=16, min_length=16)

    def clean(self):
        data = super(LoginForm, self).clean()
        try:
            user = CardUser.objects.get(number=self.cleaned_data['number'])
        except CardUser.DoesNotExist:
            raise forms.ValidationError("Such card does not exist")
        if user.is_blocked:
            raise forms.ValidationError("The card is blocked")
        return data
