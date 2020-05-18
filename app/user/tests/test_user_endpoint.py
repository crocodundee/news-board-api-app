from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


USER_CREATE_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")


class UserEndpointTests(TestCase):
    """Testing user endpoint"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating user with valid payload"""
        payload = {"username": "testuser", "password": "testpass"}
        res = self.client.post(USER_CREATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", res.data)

        exists = (
            get_user_model()
            .objects.filter(username=payload["username"])
            .exists()
        )

        self.assertTrue(exists)

    def test_create_user_failed(self):
        """Test creating user by invalid payload failed"""
        payload = {"username": "", "password": "testpass"}
        res = self.client.post(USER_CREATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_for_user(self):
        """Test creating token to auth user"""
        payload = {"username": "testuser", "password": "testpass"}
        get_user_model().objects.create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_for_user_failed(self):
        """Test token creation failed for invalid payload passed"""
        get_user_model().objects.create_user("testuser", "testpass")
        payload = {"username": "testuser", "password": "wrong"}

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_for_not_auth_user(self):
        """Test creating token failed for unknown user"""
        payload = {"username": "nousername", "password": "nopass"}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
