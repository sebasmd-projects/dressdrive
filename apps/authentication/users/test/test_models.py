#
from django.test import TestCase
#
from apps.authentication.users.models import UserModel


def general_user(self, username: str, email: str, first_name: str, last_name: str, create_admin: bool = False, password: str = "TestPassword123*"):
    """
    Function that allows you to create both regular users and administrators.

    :param self: Instance of the TestCase class.
    :param username: Username.
    :param email: Email address.
    :param first_name: Name.
    :param last_name: Last name.
    :param create_admin: Indicator if an admin user should be created. (defaults to False)
    :param password: Password. (default "TestPassword123*")
    """

    # Creation of a regular or administrator user depending on the value of the create_admin variable.
    if create_admin:
        UserModel.objects.create_superuser(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
    else:
        UserModel.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

    # Query the newly created user.
    user = UserModel.objects.filter(
        username=username
    )

    # Print user information found.
    for u in user:
        print(f"User found:")
        print(f"Full Name: {u.full_name}")
        print(f"Email: {u.email}")
        print(f"Admin: \nStaff:{u.is_staff} - Super User:{u.is_superuser}")

    # Verify that the user exists.
    self.assertTrue(
        user.exists()
    )


class UserModelTest(TestCase):
    """
    A class that contains unit tests for the user model.
    """

    def test_create_user(self):
        """
        Test to create a regular user.
        """
        general_user(
            self, "testuser",
            "testuser@sebasmd.com", "test", "user"
        )

    def test_create_superuser(self):
        """
        Test to create an administrator user.
        """
        general_user(
            self, "admintestuser",
            "admintestuser@sebasmd.com", "admin test", "user", True
        )
