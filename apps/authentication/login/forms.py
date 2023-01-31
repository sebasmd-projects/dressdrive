from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from apps.authentication.functions import password_validation
from apps.authentication.users.models import UserModel


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


class UpdatePasswordForm(forms.Form):
    password = forms.CharField(
        label=_('Current Password'),
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'id': 'update_password',
                'type': 'password',
                'placeholder': _('Current Password'),
                'class': 'form-control',
                'aria-describedby': 'update_password'
            }
        )
    )

    new_password = forms.CharField(
        label=_('New Password'),
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'id': 'update_new_password',
                'type': 'password',
                'placeholder': _('New Password'),
                'class': 'form-control',
                'aria-describedby': 'update_new_password'
            }
        )
    )

    confirm_password = forms.CharField(
        label=_('Confirm Password'),
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'id': 'update_confirm_password',
                'type': 'password',
                'placeholder': _('Confirm Password'),
                'class': 'form-control',
                'aria-describedby': 'update_confirm_password'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)
        
    
    def clean(self):
        super().clean()
        password_validation(
            self, 
            p0 = self.cleaned_data['password'],
            p1 = self.cleaned_data['new_password'],
            p2 = self.cleaned_data['confirm_password'],
            user = self.user
        )
