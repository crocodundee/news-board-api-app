from django.db import models
from django.conf import settings


class Post(models.Model):
    """News post model"""

    title = models.CharField(max_length=255, unique=True)
    link = models.URLField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(blank=True, default=0)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

    def get_link_domain(self):
        """Extract link domain"""
        domain = self.link.split('/')[2].split('.')
        return ".".join(domain[1:])

    def get_comments_total(self):
        """Get comments count"""
        return Comment.objects.filter(post__id=self.id).count()


class Comment(models.Model):
    """Posts' comment model"""

    content = models.CharField(max_length=255, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return f'Post:{self.post.id} - Author:{self.author.username}'
