from django.test import TestCase
from rest_framework.exceptions import ValidationError
from ..serializers import UserSerializer


class UserSerializerTest(TestCase):
    def test_valid_user_create(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "StrongPassword123",
            "password2": "StrongPassword123"
        }
        
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.username, data["username"])
        self.assertEqual(user.email, data["email"])
        self.assertTrue(user.check_password(data["password"]))

    def test_passwords_do_not_match(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "StrongPassword123",
            "password2": "PasswordStrong456"
        }

        serializer = UserSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        exception = context.exception
        self.assertIn("The passwords dont match", str(exception.detail))
