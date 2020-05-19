from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import (
    IsAuthenticated,
    BasePermission,
    SAFE_METHODS,
)
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Post, Comment
from news.serializers import (
    PostSerializer,
    CommentSerializer,
    PostCommentsSerializer,
)


class IsAuthorOrReadOnly(BasePermission):
    """Post author permission"""

    def has_object_permission(self, request, view, obj):
        """Check is current user is post's author"""
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class IsUpvoteUser(BasePermission):
    """Permission to upvote posts by readers"""

    def has_object_permission(self, request, view, obj):
        """Check is current user not a post author"""
        if request.user.is_authenticated:
            return obj.author != request.user
        return False


class BaseObjectViewSet(viewsets.ModelViewSet):
    """Viewset to make CRUD operations with models"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        """Create new object"""
        serializer.save(author=self.request.user)


class PostViewSet(BaseObjectViewSet):
    """
    list:
    Return a list of the exiting posts

    create:
    Create new post

    read:
    Get post detail information

    update:
    Update post information

    partial_update:
    Update some post attributes

    delete:
    Delete post from the database
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True)
    def comments(self, request, pk=None):
        """Return a list of comments relaited to post"""
        post = self.get_object()
        comments = Comment.objects.filter(post=post).order_by('created_at')
        serializer = PostCommentsSerializer(comments, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    @action(detail=True, permission_classes=[IsUpvoteUser])
    def upvote(self, request, pk=None):
        """Increate post's upvote counter"""
        post = self.get_object()
        post.upvotes += 1
        post.save()
        serializer = self.get_serializer(post)
        return Response(serializer.data, status.HTTP_200_OK)


class CommentViewSet(BaseObjectViewSet):
    """
    list:
    Return a list of all comments

    create:
    Create new comment

    read:
    Get comment's details

    update:
    Update comment content

    partial_update:
    Update some comment attributes

    delete:
    Delete comment from the database
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
