from django.urls import path
from .views import (
    CreateOrderAPIView,
    OrderListAPIView,
    OrderDetailAPIView,
    UpdateOrderStatusAPIView

)

urlpatterns = [
    path("create/", CreateOrderAPIView.as_view()),
    path("", OrderListAPIView.as_view()),
    path("<int:order_id>/", OrderDetailAPIView.as_view()),
     path("<int:order_id>/status/", UpdateOrderStatusAPIView.as_view())
]
