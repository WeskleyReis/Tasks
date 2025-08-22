from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


User = get_user_model()

class UserViewSetTest(TestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='StrongPassword123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_user_return_status_201(self):
        data = {
            "username": "testnewuser",
            "email": "test@example.com",
            "password": "StrongPassword123",
            "password2": "StrongPassword123"
        }

        url = reverse('user:user-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            User.objects.filter(username="testnewuser").exists()
        )

    def test_create_user_in_password_dont_match(self):
        data = {
            "username": "testnewuser",
            "email": "test@example.com",
            "password": "StrongPassword123",
            "password2": "PasswordStrong456"
        }

        url = reverse('user:user-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'The passwords dont match',
            str(response.json())
        )

    def test_to_update_user_data(self):
        data = {
            "username": "newnameuser",
            "current_password": "StrongPassword123"
        }

        url = reverse('user:user-detail', kwargs={'pk': self.user.pk})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual('newnameuser', self.user.username)

    def test_update_user_not_send_current_password(self):
        data = {
            "username": "newnameuser"
        }

        url = reverse('user:user-detail', kwargs={'pk': self.user.pk})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('This field is required', str(response.json()))

    def test_update_user_password_incorrect(self):
        data = {
            "username": "newnameuser",
            "current_password": "testPassword123"
        }

        url = reverse('user:user-detail', kwargs={'pk': self.user.pk})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Incorrect password', str(response.json()))

    def test_change_user_password(self):
        data = {
            "current_password": "StrongPassword123",
            "password": "NewPassword123",
            "password2": "NewPassword123"
        }

        url = reverse('user:user-change-password')
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'Password updated successfully',
            str(response.json())
        )

    def test_change_user_password_where_passwords_do_not_match(self):
        data = {
            "current_password": "StrongPassword123",
            "password": "NewPassword123",
            "password2": "PasswordNew456"
        }

        url = reverse('user:user-change-password')
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'The passwords dont match',
            str(response.json())
        )

    def test_change_user_password_do_not_send_current_password(self):
        data = {
            "password": "StrongPassword123",
            "password2": "StrongPassword123"
        }

        url = reverse('user:user-change-password')
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('This field is required', str(response.json()))

    def test_change_user_password_incorrect_password(self):
        data = {
            "current_password": "IncorrectPassword",
            "password": "StrongPassword123",
            "password2": "StrongPassword123"
        }

        url = reverse('user:user-change-password')
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Incorrect password', str(response.json()))

    def test_change_password_not_different_from_current_password(self):
        data = {
            "current_password": "StrongPassword123",
            "password": "StrongPassword123",
            "password2": "StrongPassword123"
        }
        
        url = reverse('user:user-change-password')
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'The password must be different from the current one',
            str(response.json())
        )

    def test_get_me(self):
        response = self.client.get(reverse('user:user-me'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user.username, str(response.json()))
        self.assertIn(self.user.email, str(response.json()))

    def test_login_with_email_invalid(self):
        data = {
            "email": "invalid@example.com",
            "password": "StrongPassword123"
        }

        url = reverse('user:login-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 404)
        self.assertIn('User not found', str(response.json()))

    def test_login_with_email(self):
        data = {
            "email": "test@email.com",
            "password": "StrongPassword123"
        }

        url = reverse('user:login-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
