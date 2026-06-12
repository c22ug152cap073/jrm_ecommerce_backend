from django.urls import path

from .views import (
    AddToCartAPIView,
    CartAPIView,
    UpdateCartAPIView,
    RemoveCartItemAPIView
)

urlpatterns = [
    path("add/", AddToCartAPIView.as_view()),
    path("update/", UpdateCartAPIView.as_view()),
    path("", CartAPIView.as_view()),
    path(
    "remove/",
    RemoveCartItemAPIView.as_view()
),
]