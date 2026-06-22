from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Banner
from .serializers import BannerSerializer


class BannerListAPIView(
    generics.ListAPIView
):

    queryset = Banner.objects.filter(
        is_active=True
    )

    serializer_class = BannerSerializer

    permission_classes = [AllowAny]