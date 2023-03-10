#
from django import forms

#
from django.utils.translation import gettext_lazy as _

#
from apps.authentication.functions import password_validation

#
from apps.authentication.users.models import UserModel


class UserRegisterForm(forms.ModelForm):
    CHOICES = (
        ('', '------'),
        ('M', _('Male')),
        ('F', _('Female')),
        ('O', _('Other')),

    )
    username = forms.CharField(
        label=_("User"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "id": "register_id_username",
                "type": "text",
                "placeholder": _("User"),
                "class": "form-control"
            }
        )
    )
    email = forms.CharField(
        label=_("Email"),
        required=True,
        widget=forms.EmailInput(
            attrs={
                "id": "register_id_email",
                "type": "email",
                "placeholder": _("Email"),
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        label=_('Password'),
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "id": "register_id_password",
                'type': 'password',
                'placeholder': _('Password'),
                'class': 'form-control',
            }
        )
    )
    confirm_password = forms.CharField(
        label=_('Confirm Password'),
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "id": "register_id_confirm_password",
                "type": "password",
                "placeholder": _('Confirm Password'),
                "class": "form-control",
            }
        )
    )
    first_name = forms.CharField(
        label=_("First Name"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "id": "register_id_first_name",
                "type": "text",
                "placeholder": _("First Name"),
                "class": "form-control",
            }
        )
    )
    last_name = forms.CharField(
        label=_("Last Name"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "id": "register_id_last_name",
                "type": "text",
                "placeholder": _("Last Name"),
                "class": "form-control"
            }
        )
    )
    phone = forms.CharField(
        label=_("Phone"),
        required=True,
        widget=forms.TextInput(
            attrs={
                'id': 'register_phone',
                'type': 'text',
                'placeholder': _('Phone'),
                'class': 'form-control',
                'aria-describedby': 'register_phone',
                'aria-label': _('Phone')
            }
        )
    )
    gender = forms.ChoiceField(
        choices=CHOICES,
        label=_("Gender"),
        required=True,
        widget=forms.Select(
            attrs={
                'id': 'register_gender',
                'type': 'text',
                'placeholder': _('Gender'),
                'class': 'form-select',
                'aria-describedby': 'register_gender',
                'aria-label': _('Gender')
            }
        )
    )
    birthday = forms.DateField(
        label=_("Birthday"),
        required=True,
        widget=forms.NumberInput(
            attrs={
                'id': 'register_birthday',
                'type': 'date',
                'placeholder': _('Birthday'),
                'class': 'form-control',
                'aria-describedby': 'register_birthday',
                'aria-label': _('Birthday')
            }
        )
    )
    privacy = forms.BooleanField(
        label=_('Terms & Conditions'),
        required=True,
        widget=forms.CheckboxInput(
            attrs={
                'id': 'register_id_privacy_policy',
                'type': 'checkbox',
                'class': 'form-check-input',
            }
        )
    )

    def clean_confirm_password(self):
        password_validation(
            self,
            self.cleaned_data["password"],
            self.cleaned_data["confirm_password"]
        )

    class Meta:
        model = UserModel
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "gender",
            "birthday",
            "privacy"
        )
