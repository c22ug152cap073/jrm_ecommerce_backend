from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import RecentlyViewed
from .serializers import RecentlyViewedSerializer
from products.models import Product


class AddRecentlyViewedAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        user_id = request.data.get("user_id")
        product_id = request.data.get("product_id")

        product = Product.objects.get(id=product_id)

        RecentlyViewed.objects.update_or_create(
            user_id=user_id,
            product=product
        )

        return Response({
            "message": "Product added to recently viewed"
        })


class RecentlyViewedListAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        user_id = request.query_params.get("user_id")

        items = RecentlyViewed.objects.filter(
            user_id=user_id
        )

        serializer = RecentlyViewedSerializer(
            items,
            many=True
        )

        return Response(serializer.data)