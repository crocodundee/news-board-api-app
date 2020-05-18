from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import (
    IsAuthenticated,
    BasePermission,
    SAFE_METHODS,
)

from core.models import Post
from news.serializers import PostSerializer


class IsAuthorOrReadOnly(BasePermission):
    """Post author permission"""

    def has_object_permission(self, request, view, obj):
        """Check is current user is post's author"""
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    """Endpoint to manage news posts"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        """Create new post"""
        serializer.save(author=self.request.user)
