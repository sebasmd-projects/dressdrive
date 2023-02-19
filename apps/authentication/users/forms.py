
from django import forms
from django.utils.translation import gettext_lazy as _

from apps.authentication.users.models import UserModel
from apps.authentication.functions import password_validation, email_validation


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


class UpdateProfileAvatarForm(forms.ModelForm):
    avatar = forms.ImageField(
        label=_("Profile picture"),
        required=False,
        widget=forms.FileInput(
            attrs={
                "id": "update_avatar",
                "type": "file",
                "name": "avatar",
                "accept": "image/*",
                "class": "form-control my-4"
            }
        )
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UpdateProfileAvatarForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UserModel
        fields = (
            'avatar',
        )


class UpdateProfileForm(forms.ModelForm):
    CHOICES = (
        ('', '------'),
        ('M', _('Male')),
        ('F', _('Female')),
        ('O', _('Other')),

    )
    first_name = forms.CharField(
        label=_("First Name"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'id': 'update_profile_first_name',
                'type': 'text',
                'placeholder': _('First Name'),
                'class': 'form-control',
                'aria-describedby': 'update_profile_first_name',
                'aria-label': _('First Name')
            }
        )
    )
    last_name = forms.CharField(
        label=_("Last Name"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'id': 'update_profile_last_name',
                'type': 'text',
                'placeholder': _('Last Name'),
                'class': 'form-control',
                'aria-describedby': 'update_profile_last_name',
                'aria-label': _('Last Name')
            }
        )
    )
    phone = forms.CharField(
        label=_("Phone"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'id': 'update_profile_phone',
                'type': 'text',
                'placeholder': _('Phone'),
                'class': 'form-control',
                'aria-describedby': 'update_profile_phone',
                'aria-label': _('Phone')
            }
        )
    )
    gender = forms.ChoiceField(
        choices=CHOICES,
        label=_("Gender"),
        required=False,
        widget=forms.Select(
            attrs={
                'id': 'update_profile_gender',
                'type': 'text',
                'placeholder': _('Gender'),
                'class': 'form-select',
                'aria-describedby': 'update_profile_gender',
                'aria-label': _('Gender')
            }
        )
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UpdateProfileForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UserModel
        fields = (
            'first_name',
            'last_name',
            'phone',
            'gender'
        )


class GeneralUpdateProfileForm(UpdateProfileAvatarForm, UpdateProfileForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(GeneralUpdateProfileForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UserModel
        fields = (
            'avatar',
            'first_name',
            'last_name',
            'phone',
            'gender'
        )


class UpdateNotificationsForm(forms.Form):
    pass


class PasswordResetEmailForm(forms.Form):
    email = forms.CharField(
        label=_("Email"),
        required=True,
        widget=forms.EmailInput(
            attrs={
                "id": "recover_password_email",
                "type": "email",
                "placeholder": _("Enter registered email"),
                "class": "form-control"
            }
        )
    )


class PasswordResetFormForm(forms.Form):
    password = forms.CharField(
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

    def clean(self):
        super().clean()
        try:
            password_validation(
                self,
                p1=self.cleaned_data['password'],
                p2=self.cleaned_data['confirm_password'],
            )
        except Exception:
            raise Exception
