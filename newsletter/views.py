from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Newsletter
from .serializers import NewsletterSerializer

from utils.email_service import send_notification_email


class NewsletterAPIView(
    generics.ListCreateAPIView
):

    queryset = Newsletter.objects.all().order_by(
        "-subscribed_at"
    )

    serializer_class = NewsletterSerializer

    permission_classes = [AllowAny]

    def perform_create(self, serializer):

        newsletter = serializer.save()

        send_notification_email(
            "Newsletter Subscription Successful",
            "Thank you for subscribing to our newsletter.",
            newsletter.email
        )