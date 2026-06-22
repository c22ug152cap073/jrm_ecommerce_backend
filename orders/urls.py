from django.urls import path
from .views import (
    CreateOrderAPIView,
    OrderListAPIView,
    OrderDetailAPIView,
    UpdateOrderStatusAPIView,
    ShippingAddressListCreateAPIView,
    CreatePaymentAPIView,
    GenerateInvoiceAPIView,
    CreateRazorpayOrderAPIView,


)

urlpatterns = [
    path("create/", CreateOrderAPIView.as_view()),
    path("", OrderListAPIView.as_view()),
    path("<int:order_id>/", OrderDetailAPIView.as_view()),
    path("<int:order_id>/status/", UpdateOrderStatusAPIView.as_view()),
     path(
        "shipping-address/",
        ShippingAddressListCreateAPIView.as_view()
    ),
    path(
    "payment/",
    CreatePaymentAPIView.as_view()
),
    path(
    "invoice/",
    GenerateInvoiceAPIView.as_view()
),
path(
    "razorpay/create-order/",
    CreateRazorpayOrderAPIView.as_view()
),
]
