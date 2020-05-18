from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import (
    IsAuthenticated,
    BasePermission,
    SAFE_METHODS,
)

from core.models import Post, Comment
from news.serializers import PostSerializer, CommentSerializer


class IsAuthorOrReadOnly(BasePermission):
    """Post author permission"""

    def has_object_permission(self, request, view, obj):
        """Check is current user is post's author"""
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class BaseObjectViewSet(viewsets.ModelViewSet):
    """Viewset to make CRUD operations with models"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        """Create new object"""
        serializer.save(author=self.request.user)


class PostViewSet(BaseObjectViewSet):
    """Endpoint to manage news posts"""

    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(BaseObjectViewSet):
    """Endpoint to manage comments"""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
