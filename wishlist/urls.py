from django.urls import path

from .views import (
    WishlistListAPIView,
    AddToWishlistAPIView,
    RemoveWishlistAPIView
)

urlpatterns = [

    path(
        "",
        WishlistListAPIView.as_view()
    ),

    path(
        "add/",
        AddToWishlistAPIView.as_view()
    ),

    path(
        "remove/",
        RemoveWishlistAPIView.as_view()
    ),

]