from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Contact
from .serializers import ContactSerializer


class ContactAPIView(
    generics.ListCreateAPIView
):

    queryset = Contact.objects.all().order_by(
        "-created_at"
    )

    serializer_class = ContactSerializer

    permission_classes = [AllowAny]