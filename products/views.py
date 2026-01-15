# products/views/py
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)

from .models import Product
from .serializers import ProductSerializer


class ListProductAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


class RetrieveProductAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]


class CreateProductAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]


class UpdateProductAPIView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminUser]


class DestroyProductAPIView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminUser]
