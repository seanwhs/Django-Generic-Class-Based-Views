# products/urls.py
from django.urls import path
from .views import (
    ListProductAPIView,
    CreateProductAPIView,
    RetrieveProductAPIView,
    UpdateProductAPIView,
    DestroyProductAPIView,
)

urlpatterns = [
    path('products/', ListProductAPIView.as_view(), name = 'product-list'),
    path('products/create', CreateProductAPIView.as_view(), name = 'product-create'),
    path('products/retrieve/<slug:slug>', RetrieveProductAPIView.as_view(), name = 'product-retrieve'),
    path('products/update/<slug:slug>', UpdateProductAPIView.as_view(), name = 'product-update'),
    path('products/destroy/<slug:slug>', DestroyProductAPIView.as_view(), name = 'product-destroy'),
]