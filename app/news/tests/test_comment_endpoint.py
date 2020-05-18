from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Post, Comment
from news.serializers import CommentSerializer


COMMENT_URL = reverse('news:comment-list')


def detail_url(comment_id):
    """Create and return post's detail url"""
    return reverse('news:comment-detail', args=[comment_id])


class CommentEndpointTests(TestCase):
    """Tests CRUD Comment operations"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'postauthor', 'authorpass'
        )
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(
            title='Base post',
            link='http://www.base-link.org',
            author=self.user,
        )

    def test_comment_listed(self):
        """Test listing all created comments"""
        Comment.objects.create(
            content='Great post!', post=self.post, author=self.user
        )
        Comment.objects.create(
            content='Super!', post=self.post, author=self.user
        )

        comments = Comment.objects.all()

        res = self.client.get(COMMENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        serializer = CommentSerializer(comments, many=True)

        self.assertEqual(serializer.data, res.data)
        self.assertEqual(len(res.data), 2)

    def test_comment_create(self):
        """Test create post by user"""
        payload = {'content': 'Awesome news!', 'post': self.post.id}

        res = self.client.post(COMMENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        exists = Comment.objects.filter(content=payload['content']).exists()
        self.assertTrue(exists)

        payload = {'content': ''}
        res = self.client.post(COMMENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_update(self):
        """Test user can update comment"""
        comment = Comment.objects.create(
            content='Great post', post=self.post, author=self.user
        )
        payload = {'content': 'Ugly content'}

        url = detail_url(comment.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        comment.refresh_from_db()
        self.assertEqual(comment.content, payload['content'])

    def test_comment_delete(self):
        """Test user can delete his comment"""
        comment = Comment.objects.create(
            content='Simple comment', post=self.post, author=self.user
        )

        url = detail_url(comment.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        exists = Comment.objects.filter(content=comment.content).exists()
        self.assertFalse(exists)


class UserLimitationOnUpdateOperationsTests(TestCase):
    """Tests user permissions required for update methods"""

    def setUp(self):
        self.client = APIClient()
        self.author = get_user_model().objects.create_user(
            'postauthor', 'authorpass'
        )
        self.post = Post.objects.create(
            title='My post', link='https://www.github.com', author=self.author
        )
        self.comment = Comment.objects.create(
            content='Simple comment', post=self.post, author=self.author
        )
        self.user = get_user_model().objects.create_user(
            'testuser', 'testpass'
        )
        self.client.force_authenticate(user=self.user)

    def test_user_cannot_update_other_author_comments(self):
        """Test user unavailable to update other author comment"""
        payload = {
            'content': 'I wont update your comment!',
        }

        url = detail_url(self.comment.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
