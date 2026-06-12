from rest_framework import generics

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import (
    Category,
    Product
)

from .serializers import (
    CategorySerializer,
    ProductSerializer
)


class CategoryListAPIView(
    generics.ListCreateAPIView
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListAPIView(
    generics.ListCreateAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "category",
        "is_active",
    ]

    search_fields = [
        "name",
        "description",
        "sku",
    ]

    ordering_fields = [
        "price",
        "created_at",
    ]


class ProductDetailAPIView(
    generics.RetrieveAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer