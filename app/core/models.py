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
