from django.urls import path

from .views import (
    CategoryListAPIView,
    ProductListAPIView,
    ProductDetailAPIView,
    ProductSearchAPIView
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
     path("search/", ProductSearchAPIView.as_view()),
]