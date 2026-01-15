# posts/models.py
from django.db import models

class Post(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # Always know when it happened