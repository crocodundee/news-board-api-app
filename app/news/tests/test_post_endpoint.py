from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Post
from news.serializers import PostSerializer


POST_URL = reverse('news:post-list')


def detail_url(post_id):
    """Create and return post's detail url"""
    return reverse('news:post-detail', args=[post_id])


class PostEndpointTests(TestCase):
    """Tests CRUD Post operations"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'postauthor', 'authorpass'
        )
        self.client.force_authenticate(user=self.user)

    def test_post_listed(self):
        """Test listing all created posts"""
        Post.objects.create(
            title='Post 1', link='freebsd.org', author=self.user
        )
        Post.objects.create(
            title='Post 2', link='kgbase.com', author=self.user
        )

        posts = Post.objects.all()

        res = self.client.get(POST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        serializer = PostSerializer(posts, many=True)

        self.assertEqual(serializer.data, res.data)
        self.assertEqual(len(res.data), 2)

    def test_post_create(self):
        """Test create post by user"""
        payload = {
            'title': 'Awesome news!',
            'link': 'wsj.com',
        }

        res = self.client.post(POST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        exists = Post.objects.filter(title=payload['title']).exists()

        self.assertTrue(exists)

    def test_post_update(self):
        """Test user can update post"""
        post = Post.objects.create(
            title='New post', link='wiki.org', author=self.user
        )
        payload = {'title': 'Updated post title'}

        url = detail_url(post.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        post.refresh_from_db()

        self.assertEqual(post.title, payload['title'])

    def test_post_delete(self):
        """Test user can delete his post"""
        post = Post.objects.create(
            title='My post', link='newssite.com', author=self.user
        )

        url = detail_url(post.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        exists = Post.objects.filter(title=post.title).exists()
        self.assertFalse(exists)


class UserLimitationOnUpdateOperationsTests(TestCase):
    """Tests user permissions required for update methods"""

    def setUp(self):
        self.client = APIClient()
        self.author = get_user_model().objects.create_user(
            'postauthor', 'authorpass'
        )
        self.post = Post.objects.create(
            title='My post', link='github.com', author=self.author
        )
        self.user = get_user_model().objects.create_user(
            'testuser', 'testpass'
        )
        self.client.force_authenticate(user=self.user)

    def test_user_cannot_update_other_author_posts(self):
        """Test user unavailable to update other author post"""
        payload = {'title': 'Not your post', 'link': 'bitbucket.com'}

        url = detail_url(self.post.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
