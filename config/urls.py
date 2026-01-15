# root urls.py
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('products.urls')),
    path('api/', include('posts.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
