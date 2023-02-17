from django import forms
from django.utils.translation import gettext_lazy as _

from apps.authentication.functions import password_validation, email_validation
from apps.authentication.users.models import UserModel

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
        try:
            password_validation(
                self,
                p0=self.cleaned_data['password'],
                p1=self.cleaned_data['new_password'],
                p2=self.cleaned_data['confirm_password'],
                user=self.user
            )
        except Exception:
            raise Exception


class UpdateEmailForm(forms.Form):
    new_email = forms.CharField(
        label=_("New Email"),
        required=True,
        widget=forms.EmailInput(
            attrs={
                "id": "update_new_email",
                "type": "email",
                "placeholder": _("New Email"),
                "class": "form-control"
            }
        )
    )

    confirm_email = forms.CharField(
        label=_("Confirm Email"),
        required=True,
        widget=forms.EmailInput(
            attrs={
                "id": "confirm_email",
                "type": "email",
                "placeholder": _("Confirm Email"),
                "class": "form-control"
            }
        )
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UpdateEmailForm, self).__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        try:
            email_validation(
                self,
                email1=self.cleaned_data['new_email'],
                email2=self.cleaned_data['confirm_email'],
                user=self.user
            )
        except Exception:
            raise Exception


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    
    
    class Meta:
        model = UserModel
        fields = (
            'avatar',
            'first_name',
            'last_name',
            'location',
            'latitude',
            'longitude',
            'phone'
        )

class UpdateNotificationsForm(forms.Form):
    pass