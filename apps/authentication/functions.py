#
import re
#
from django.utils.translation import gettext_lazy as _


def password_validation(self, p1, p2, p0=None, user=None):
    """
    This function performs password validation for a user.
    If a user is provided, it will check if the current password provided is correct and 
    if the new password is the same as the old password.
    It will then validate the new password against the following requirements:
    - At least 6 characters long
    - Must contain at least 1 lowercase letter
    - Must contain at least 1 uppercase letter
    - Must contain at least 1 number
    - Must contain at least 1 special character
    Finally, it will check if the new password and the password confirmation match.

    Parameters:
    self (object): The current instance of the form being validated
    p1 (str): The new password provided
    p2 (str): The password confirmation provided
    p0 (str, optional): The current password of the user. Defaults to None.
    user (django.contrib.auth.models.User, optional): The user being validated. Defaults to None.

    Returns:
    None: Adds error messages to the form instance in case of validation failures
    """
    if user:
        # Check if the current password provided is correct
        if not user.check_password(self.cleaned_data['password']):
            self.add_error(
                "password",
                _("Incorrect current password")
            )
        # Check if the new password is the same as the old password
        if p1 == p0:
            self.add_error(
                "password",
                _("The password can not be the same")
            )
    # Check if the new password meets the requirements
    if not re.match(r'^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)(?=.*?[^\w\s])[^\s]{6,}$', p1):
        self.add_error(
            'confirm_password',
            _(
                "The password must have: At least 6 characters. A letter in minus. A letter in mayus. A number. A special character."
            )
        )
    # Check if the new password and the password confirmation match
    if p1 != p2:
        self.add_error(
            "confirm_password",
            _("Passwords don't match")
        )
