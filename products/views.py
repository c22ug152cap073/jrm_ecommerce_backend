from rest_framework import generics

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import AllowAny

from .models import (
    Category,
    Product
)

from .serializers import (
    CategorySerializer,
    ProductSerializer
)


class CategoryListAPIView(
    generics.ListAPIView
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ProductListAPIView(
    generics.ListAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

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
    "category__name",
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
    permission_classes = [AllowAny]

class ProductSearchAPIView(generics.ListAPIView):

    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        keyword = self.request.GET.get("q")

        if keyword:
            return Product.objects.filter(
                name__icontains=keyword
            )

        return Product.objects.none()