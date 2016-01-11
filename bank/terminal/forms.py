from django import forms
from django.contrib.auth import authenticate

from .models import CardUser
from .models import Transaction


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


class WithdrawMoneyForm(forms.Form):
    amount = forms.IntegerField(min_value=0)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super(WithdrawMoneyForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = super(WithdrawMoneyForm, self).clean()
        amount = self.cleaned_data.get('amount')
        if not self.instance or not amount:
            return data
        if amount > self.instance.balance:
            raise forms.ValidationError("Insufficient balance")
        return data

    def save(self):
        if self.is_valid():
            self.instance.balance -= self.cleaned_data['amount']
            self.instance.save()
            Transaction.objects.create(
                operation='WD',
                card=self.instance,
                amount=self.cleaned_data['amount'],
            )
