from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Wishlist
from .serializers import WishlistSerializer


class WishlistListAPIView(
    generics.ListAPIView
):

    serializer_class = WishlistSerializer

    permission_classes = [AllowAny]

    def get_queryset(self):

        user_id = self.request.GET.get(
            "user_id"
        )

        return Wishlist.objects.filter(
            user_id=user_id
        ).order_by("-created_at")


class AddToWishlistAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = WishlistSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response({
            "message": "Added to wishlist"
        })


class RemoveWishlistAPIView(APIView):

    permission_classes = [AllowAny]

    def delete(self, request):

        user_id = request.data.get(
            "user_id"
        )

        product_id = request.data.get(
            "product_id"
        )

        item = Wishlist.objects.filter(
            user_id=user_id,
            product_id=product_id
        ).first()

        if not item:
            return Response({
                "error": "Wishlist item not found"
            }, status=404)

        item.delete()

        return Response({
            "message": "Removed from wishlist"
        })