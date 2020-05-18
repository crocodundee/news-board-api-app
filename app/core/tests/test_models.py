from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Post


class ModelsTests(TestCase):
    """Test application models"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'testuser', 'testpass'
        )

    def test_post_create_success(self):
        """Test create post model"""

        post = Post.objects.create(
            title='My first post', link="It's great news!", author=self.user
        )

        self.assertEqual(str(post), post.title)
