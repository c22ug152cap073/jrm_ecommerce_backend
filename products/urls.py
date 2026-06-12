from django.urls import path

from .views import (
    CategoryListAPIView,
    ProductListAPIView,
    ProductDetailAPIView
)

urlpatterns = [
    path(
        "categories/",
        CategoryListAPIView.as_view()
    ),

    path(
        "",
        ProductListAPIView.as_view()
    ),

    path(
        "<int:pk>/",
        ProductDetailAPIView.as_view()
    ),
]