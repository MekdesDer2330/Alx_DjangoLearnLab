from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from .models import Like, Post, Comment,Like
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType
from .serializers import PostSerializer, CommentSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit/delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for the owner
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if created:
        # create notification
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            target=post
        )
        return Response({'message': 'Post liked'})
    return Response({'message': 'You already liked this post'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like = Like.objects.filter(user=request.user, post=post).first()
    if like:
        like.delete()
        return Response({'message': 'Post unliked'})
    return Response({'message': 'You have not liked this post'}, status=400)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def feed_view(request):
    following_users = request.user.following.all()
    feed_posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    serializer = PostSerializer(feed_posts, many=True)
    return Response(serializer.data)