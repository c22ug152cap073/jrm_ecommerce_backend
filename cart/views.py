from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Cart, CartItem
from products.models import Product

from .serializers import (
    AddToCartSerializer,
    CartItemSerializer
)


class AddToCartAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = AddToCartSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        product = Product.objects.get(
            id=serializer.validated_data["product_id"]
        )

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if not created:
            item.quantity += serializer.validated_data["quantity"]

        item.save()

        return Response({
            "message": "Product added to cart"
        })


class CartAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        cart = Cart.objects.filter(
            user=request.user
        ).first()

        if not cart:
            return Response([])

        serializer = CartItemSerializer(
            cart.items.all(),
            many=True
        )

        return Response(serializer.data)


class UpdateCartAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):

        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        cart = Cart.objects.filter(
            user=request.user
        ).first()

        if not cart:
            return Response(
                {"error": "Cart not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        item = CartItem.objects.filter(
            cart=cart,
            product_id=product_id
        ).first()

        if not item:
            return Response(
                {"error": "Product not found in cart"},
                status=status.HTTP_404_NOT_FOUND
            )

        item.quantity = quantity
        item.save()

        return Response({
            "message": "Cart updated successfully"
        })
class RemoveCartItemAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request):

        product_id = request.data.get("product_id")

        cart = Cart.objects.filter(
            user=request.user
        ).first()

        if not cart:
            return Response(
                {"error": "Cart not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        item = CartItem.objects.filter(
            cart=cart,
            product_id=product_id
        ).first()

        if not item:
            return Response(
                {"error": "Product not found in cart"},
                status=status.HTTP_404_NOT_FOUND
            )

        item.delete()

        return Response({
            "message": "Product removed from cart"
        })