# posts/urls.py
from django.urls import path
from .views import (
    ListCreatePostAPIView,
    RetrieveUpdateDestroyPostAPIView,
)

urlpatterns = [
    path('posts/', ListCreatePostAPIView.as_view(), name = 'post-list-create'),
    path('posts/<int:pk>', RetrieveUpdateDestroyPostAPIView.as_view(), name = 'post-retreive-update-destroy'),
]