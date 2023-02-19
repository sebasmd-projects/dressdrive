#
from django.test import TestCase
#
from apps.authentication.register.forms import (
    UserRegisterForm
)


def output(self, form, assertType=False):
    print(f"Form: {form.data}")
    if form.errors:
        print(f"Output: {form.errors}")
    if assertType:
        self.assertTrue(form.is_valid())
    else:
        self.assertFalse(form.is_valid())


class UserRegisterFormTest(TestCase):

    def setUp(self) -> None:
        """
        Data to use in all tests
        """
        self.userForm = {
            "username": "testuser",
            "email": "testuser@sebasmd.com",
            "first_name": "test",
            "last_name": "user",
            "phone": "3000000000",
            "gender": "O",
            "birthday": "16/05/1999",
            "privacy": "True"
        }

    def test_valid_register_form(self):
        """
        Test for a valid sign up 
        """
        form = UserRegisterForm({
            **self.userForm,
            "password": "TestPassword123*",
            "confirm_password": "TestPassword123*",
        })
        output(self, form, assertType=True)

    def test_invalid_register_form_password_dont_match(self):
        """
        Test for an invalid password match
        """
        form = UserRegisterForm({
            **self.userForm,
            "password": "TestPassword123!",
            "confirm_password": "TestPassword123*",
        })
        output(self, form)

    def test_invalid_register_form_length(self):
        """
        Test for an invalid password length
        """
        form = UserRegisterForm({
            **self.userForm,
            "password": "12345",
            "confirm_password": "12345",
        })
        output(self, form)

    def test_invalid_register_form_mayus(self):
        """
        Test for an invalid only minus chars
        """
        form = UserRegisterForm({
            **self.userForm,
            "password": "testpassword123*",
            "confirm_password": "testpassword123*"
        })
        output(self, form)

    def test_invalid_register_form_minus(self):
        """
        Test for an invalid only mayus chars
        """
        form = UserRegisterForm({
            **self.userForm,
            "password": "TESTPASSWORD123*",
            "confirm_password": "TESTPASSWORD123*",
        })
        output(self, form)

    def test_invalid_register_form_number(self):
        """
        Test for an invalid no numbers
        """
        form = UserRegisterForm({
            **self.userForm,
            "password": "TestPassword*",
            "confirm_password": "TestPassword*",
        })
        output(self, form)

    def test_invalid_register_form_special_char(self):
        """
        Test for an invalid no special chars
        """
        form = UserRegisterForm({
            **self.userForm,
            "password": "TestPassword123",
            "confirm_password": "TestPassword123",
        })
        output(self, form)
