#
from django.test import TestCase, Client
#
from django.urls import reverse
#
from apps.authentication.users.models import UserModel


class UserRegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse("authentication_register:user-register")
        self.valid_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'password123*',
            'privacy': True
        }

    def test_view_uses_correct_template(self):
        response = self.client.get(self.register_url)
        self.assertTemplateUsed(response, "authentication/register.html")

    def test_register_invalid(self):
        invalid_data = {
            'username': '',
            'email': '',
            'first_name': '',
            'last_name': '',
            'password': '',
            'privacy': True
        }
        response = self.client.post(self.register_url, data=invalid_data)
        self.assertEqual(response.status_code, 200)  # stay on the same page
        self.assertFalse(
            UserModel.objects.filter(
                username=invalid_data['username']).exists()
        )
