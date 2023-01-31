import re
from django.utils.translation import gettext_lazy as _


def change_password_validation(self, p1, p2, user):
    if user:
        if not user.check_password(self.cleaned_data['password']):
            self.add_error(
                "password",
                _("Incorrect current password")
            )

    if not re.match(r'^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)(?=.*?[^\w\s])[^\s]{6,}$', p1):
        self.add_error(
            'confirm_password',
            _(
                "The password must have: At least 6 characters. A letter in minus. A letter in mayus. A number. A special character."
            )
        )

    if p1 != p2:
        self.add_error(
            "confirm_password",
            _("Passwords don't match")
        )
