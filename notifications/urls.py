from django.urls import path
from .views import TestEmailAPIView

urlpatterns = [
    path(
        "test/",
        TestEmailAPIView.as_view()
    ),
]