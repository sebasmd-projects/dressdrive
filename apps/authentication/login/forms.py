from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class UserLoginForm(forms.Form):
    username = forms.CharField(
        label=_('Email or Username'),
        required=True,
        widget=forms.TextInput(
            attrs={
                'id': 'login_email_or_username',
                'type': 'text',
                'placeholder': _('Email or Username'),
                'class': 'form-control',
                'aria-label': _('Email or Username'),
                'aria-describedby': 'emailLogin'
            },
        )
    )

    password = forms.CharField(
        label=_('Password'),
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'id': 'login_password',
                'type': 'password',
                'placeholder': _('Password'),
                'class': 'form-control',
                'aria-label': _('Password'),
                'aria-describedby': 'login_password'
            }
        )
    )

    remember_me = forms.BooleanField(
        label=_('Remember password'),
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'id': 'login_remember_me',
                'type': 'checkbox',
                'class': 'form-check-input',
            }
        )
    )

    def clean(self):
        cleaned_data = super(UserLoginForm, self).clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not authenticate(username=username, password=password):
            raise forms.ValidationError(
                _('The credentials are invalid')
            )

        return self.cleaned_data
