from django.test import TestCase
from rest_framework.exceptions import ValidationError
from ..serializers import UserChangePasswordSerializer
from django.contrib.auth import get_user_model


User = get_user_model()

class UserChangePasswordSerializerTest(TestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username='testuser',
            password='StrongPassword123'
        )

    def test_valid_password_change(self):
        data = {
            "id": 1,
            "password": "NewPassword123",
            "password2": "NewPassword123"
        }

        serializer = UserChangePasswordSerializer(instance=self.user, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.assertTrue(self.user.check_password("NewPassword123"))

    def test_new_password_must_be_different(self):
        data = {
            "id": 1,
            "password": "StrongPassword123",
            "password2": "StrongPassword123"
        }

        serializer = UserChangePasswordSerializer(instance=self.user, data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
            serializer.save()

        exception = context.exception
        self.assertIn(
            "The password must be different from the current one",
            str(exception.detail)
        )

    def test_password_do_not_match(self):
        data = {
            "id": 1,
            "password": "Password123",
            "password2": "Password456"
        }

        serializer = UserChangePasswordSerializer(instance=self.user, data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        exception = context.exception
        self.assertIn("The passwords dont match", str(exception.detail))