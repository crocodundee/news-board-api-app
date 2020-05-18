from rest_framework import serializers

from core.models import Post


class PostSerializer(serializers.ModelSerializer):
    """Serializer for news post"""

    class Meta:
        model = Post
        fields = ('id', 'title', 'link', 'created_at', 'author', 'upvotes')
        read_only_fields = ('id', 'created_at', 'upvotes', 'author')
