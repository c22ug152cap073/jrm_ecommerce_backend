from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Newsletter
from .serializers import NewsletterSerializer


class NewsletterAPIView(
    generics.ListCreateAPIView
):

    queryset = Newsletter.objects.all().order_by(
        "-subscribed_at"
    )

    serializer_class = NewsletterSerializer

    permission_classes = [AllowAny]