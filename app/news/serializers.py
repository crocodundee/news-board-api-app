from rest_framework import serializers

from core.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    """Serializer for news post"""

    class Meta:
        model = Post
        fields = ('id', 'title', 'link', 'created_at', 'author', 'upvotes')
        read_only_fields = ('id', 'created_at', 'upvotes', 'author')


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comment"""

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'author')


class PostCommentsSerializer(serializers.ModelSerializer):
    """Serializer for listing comments relaited to post"""

    class Meta:
        model = Comment
        fields = ('id', 'created_at', 'content', 'author')
        read_only_fields = ('id', 'created_at', 'content', 'author')
