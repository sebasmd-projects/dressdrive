#
from django.test import TestCase
#
from apps.authentication.register.forms import (
    UserRegisterForm
)



def output(self, form, assertType=False):
    print(f"Form: {form.data}")
    if form.errors:
        print(f"Output: {form.errors['confirm_password']}")
    if assertType:
        self.assertTrue(form.is_valid())
    else:
        self.assertFalse(form.is_valid())


class UserRegisterFormTest(TestCase):

    userForm = {
        "username": "testuser",
        "email": "testuser@sebasmd.com",
        "first_name": "test",
        "last_name": "user",
        "privacy": "True"
    }

    def test_valid_register_form(self):
        form = UserRegisterForm({
            **self.userForm,
            "password": "TestPassword123*",
            "confirm_password": "TestPassword123*",

        })
        output(self, form, True)

    def test_invalid_register_form_password_dont_match(self):
        form = UserRegisterForm({
            **self.userForm,
            "password": "TestPassword123!",
            "confirm_password": "TestPassword123*",
        })
        output(self, form)

    def test_invalid_register_form_length(self):
        form = UserRegisterForm({
            **self.userForm,
            "password": "12345",
            "confirm_password": "12345",
        })
        output(self, form)

    def test_invalid_register_form_mayus(self):
        form = UserRegisterForm({
            **self.userForm,
            "password": "testpassword123*",
            "confirm_password": "testpassword123*",
        })
        output(self, form)

    def test_invalid_register_form_minus(self):
        form = UserRegisterForm({
            **self.userForm,
            "password": "TESTPASSWORD123*",
            "confirm_password": "TESTPASSWORD123*",
        })
        output(self, form)

    def test_invalid_register_form_number(self):
        form = UserRegisterForm({
            **self.userForm,
            "password": "TestPassword*",
            "confirm_password": "TestPassword*",
        })
        output(self, form)

    def test_invalid_register_form_special_char(self):
        form = UserRegisterForm({
            **self.userForm,
            "password": "TestPassword123",
            "confirm_password": "TestPassword123",
        })
        output(self, form)
