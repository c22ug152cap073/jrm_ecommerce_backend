from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Review
from .serializers import ReviewSerializer


class ReviewListCreateAPIView(
    generics.ListCreateAPIView
):

    queryset = Review.objects.all().order_by("-created_at")

    serializer_class = ReviewSerializer

    permission_classes = [AllowAny]