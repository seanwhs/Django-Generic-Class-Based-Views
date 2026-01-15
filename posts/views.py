# posts/views.py
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .models import Post
from .serializers import PostSerializer


class ListCreatePostAPIView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class RetrieveUpdateDestroyPostAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
