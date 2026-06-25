from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Contact
from .serializers import ContactSerializer
from utils.email_service import send_notification_email


class ContactAPIView(
    generics.ListCreateAPIView
):

    queryset = Contact.objects.all().order_by(
        "-created_at"
    )

    serializer_class = ContactSerializer

    permission_classes = [AllowAny]

    def perform_create(self, serializer):

        contact = serializer.save()

        send_notification_email(
            "Contact Request Received",
            "We have received your message and will contact you soon.",
            contact.email
        )