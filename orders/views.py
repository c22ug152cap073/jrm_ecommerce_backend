from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from cart.models import Cart
from .models import Order, OrderItem


class CreateOrderAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        user_id = request.data.get("user_id")

        cart = Cart.objects.filter(
            user_id=user_id
        ).first()

        if not cart:
            return Response({
                "error": "Cart is empty"
            })

        order = Order.objects.create(
            user_id=user_id
        )

        total = 0

        for item in cart.items.all():

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

            total += item.product.price * item.quantity

        order.total_amount = total
        order.save()

        cart.items.all().delete()

        return Response({
            "message": "Order placed successfully",
            "order_id": order.id,
            "total_amount": total
        })
from .models import Order


class OrderListAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        orders = Order.objects.all()

        data = []

        for order in orders:
            data.append({
                "id": order.id,
                "user_id": order.user.id,
                "email": order.user.email,
                "total_amount": order.total_amount,
                "status": order.status,
                "created_at": order.created_at
            })

        return Response(data)

class OrderDetailAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, order_id):

        order = Order.objects.filter(
            id=order_id
        ).first()

        if not order:
            return Response({
                "error": "Order not found"
            }, status=404)

        items = []

        for item in order.items.all():

            items.append({
                "product_id": item.product.id,
                "product_name": item.product.name,
                "quantity": item.quantity,
                "price": item.price
            })

        return Response({
            "id": order.id,
            "user_id": order.user.id,
            "email": order.user.email,
            "total_amount": order.total_amount,
            "status": order.status,
            "created_at": order.created_at,
            "items": items
        })
class UpdateOrderStatusAPIView(APIView):

    permission_classes = [AllowAny]

    def put(self, request, order_id):

        status_value = request.data.get("status")

        order = Order.objects.filter(
            id=order_id
        ).first()

        if not order:
            return Response({
                "error": "Order not found"
            }, status=404)

        order.status = status_value
        order.save()

        return Response({
            "message": "Order status updated",
            "status": order.status
        })