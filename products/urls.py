from django.urls import path

from .views import (
    CategoryListAPIView,
    ProductListAPIView,
    ProductDetailAPIView,
    ProductSearchAPIView,
    ProductRecommendationAPIView,
    FeaturedProductsAPIView,
    NewArrivalsAPIView,
    CustomersAlsoBoughtAPIView,
    SimilarPriceProductsAPIView,
    PersonalizedRecommendationAPIView,
    LowStockProductsAPIView,
    OutOfStockProductsAPIView,
    InventoryDashboardAPIView,
    BestSellerProductsAPIView,
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
    path(
    "recommendations/<int:product_id>/",
    ProductRecommendationAPIView.as_view()),
    path(
    "featured/",
    FeaturedProductsAPIView.as_view()),
    path(
    "new-arrivals/",
    NewArrivalsAPIView.as_view()),
    path(
    "customers-also-bought/<int:product_id>/",
    CustomersAlsoBoughtAPIView.as_view()),
    path(
    "similar-price/<int:product_id>/",
    SimilarPriceProductsAPIView.as_view()),
    path(
    "personalized/",
    PersonalizedRecommendationAPIView.as_view()),
    path(
    "low-stock/",
    LowStockProductsAPIView.as_view()),
    path(
    "out-of-stock/",
    OutOfStockProductsAPIView.as_view()),
    path(
    "inventory/dashboard/",
    InventoryDashboardAPIView.as_view()),
]