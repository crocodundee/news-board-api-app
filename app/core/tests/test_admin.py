from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


ADMIN_URL = reverse('admin:index')
USER_ADMIN_URL = reverse('admin:auth_user_changelist')
ADMIN_LOGIN = reverse('admin:login')


class UserAdminTests(TestCase):
    """Tests for UserAdmin"""

    def setUp(self):
        self.client = Client()
        self.admin = get_user_model().objects.create_superuser(
            username='admin',
            password='adminpass',
            email='admin@company.com'
        )
        self.client.force_login(user=self.admin)

    def test_admin_access_to_site(self):
        """Test admin page is available for admin"""
        res = self.client.get(ADMIN_URL)

        self.assertEqual(res.status_code, 200)

    def test_user_admin_page(self):
        """Test is UserAdminPage is available"""
        res = self.client.get(USER_ADMIN_URL)

        self.assertEqual(res.status_code, 200)


class UserAdminPublicUsersTests(TestCase):
    """Test UserAdmin via public users"""

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            'testuser', 'testpass'
        )
        self.client.force_login(user=self.user)

    def test_admin_page_not_available(self):
        """Testing nostaff user cannot access to admin page"""
        res = self.client.get(ADMIN_URL)

        self.assertEqual(res.status_code, 302)
