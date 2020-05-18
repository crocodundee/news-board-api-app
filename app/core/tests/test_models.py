from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Post, Comment


class ModelsTests(TestCase):
    """Test application models"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'testuser', 'testpass'
        )

    def test_post_create_success(self):
        """Test create post model"""

        post = Post.objects.create(
            title='My first post',
            link="https://www.news.com",
            author=self.user,
        )

        self.assertEqual(str(post), post.title)

    def test_create_comment_success(self):
        """Test create comment model"""
        post = Post.objects.create(
            title='My second post',
            link='http://www.my-blog.ua',
            author=self.user,
        )

        comment = Comment.objects.create(
            content='So wonderful post', post=post, author=self.user
        )
        expected = f'Post:{comment.post.id} - Author:{comment.author.username}'
        self.assertEqual(str(comment), expected)
