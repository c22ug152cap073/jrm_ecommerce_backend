from django.urls import path
from .views import NewsletterAPIView

urlpatterns = [
    path(
        "",
        NewsletterAPIView.as_view()
    ),
]