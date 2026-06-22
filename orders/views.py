from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from cart.models import Cart
from .models import Order, OrderItem, Payment,Invoice
from rest_framework import generics
from .models import ShippingAddress
from .serializers import ShippingAddressSerializer,PaymentSerializer,InvoiceSerializer
import razorpay
from django.conf import settings


class CreateOrderAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        user_id = request.data.get("user_id")
        shipping_address_id = request.data.get("shipping_address_id")

        shipping_address = ShippingAddress.objects.filter(
            id=shipping_address_id
        ).first()

        if not shipping_address:
            return Response({
                "error": "Invalid shipping address"
            }, status=400)

        cart = Cart.objects.filter(
            user_id=user_id
        ).first()

        if not cart:
            return Response({
                "error": "Cart is empty"
            })

        order = Order.objects.create(
        user_id=user_id,
        shipping_address=shipping_address
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
            "shipping_address": {
                "full_name": order.shipping_address.full_name if order.shipping_address else None,
                "phone": order.shipping_address.phone if order.shipping_address else None,
                "address": order.shipping_address.address if order.shipping_address else None,
                "city": order.shipping_address.city if order.shipping_address else None,
                "state": order.shipping_address.state if order.shipping_address else None,
                "pincode": order.shipping_address.pincode if order.shipping_address else None,
                "country": order.shipping_address.country if order.shipping_address else None,
            },
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
class ShippingAddressListCreateAPIView(
    generics.ListCreateAPIView
):

    queryset = ShippingAddress.objects.all()

    serializer_class = ShippingAddressSerializer

class CreatePaymentAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        order_id = request.data.get("order_id")
        payment_method = request.data.get("payment_method")

        order = Order.objects.filter(
            id=order_id
        ).first()

        if not order:
            return Response(
                {"error": "Order not found"},
                status=404
            )

        payment = Payment.objects.create(
            order=order,
            payment_method=payment_method,
            payment_status="Success",
            transaction_id=f"TXN{order.id}"
        )

        return Response({
            "message": "Payment Successful",
            "payment_id": payment.id,
            "transaction_id": payment.transaction_id
        })
class GenerateInvoiceAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        payment_id = request.data.get("payment_id")

        payment = Payment.objects.filter(
            id=payment_id
        ).first()

        if not payment:
            return Response({
                "error": "Payment not found"
            }, status=404)

        invoice = Invoice.objects.create(
            order=payment.order,
            payment=payment,
            invoice_number=f"INV{payment.id}",
            total_amount=payment.order.total_amount
        )

        return Response({
            "message": "Invoice Generated",
            "invoice_number": invoice.invoice_number
        })
class CreateRazorpayOrderAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        order_id = request.data.get("order_id")

        order = Order.objects.filter(
            id=order_id
        ).first()

        if not order:
            return Response(
                {"error": "Order not found"},
                status=404
            )

        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            )
        )

        razorpay_order = client.order.create({
            "amount": int(order.total_amount * 100),
            "currency": "INR",
            "payment_capture": 1
        })

        payment, created = Payment.objects.get_or_create(
            order=order,
            defaults={
                "payment_method": "RAZORPAY",
                "payment_status": "Pending",
                "razorpay_order_id": razorpay_order["id"]
            }
        )

        if not created:
            payment.payment_method = "RAZORPAY"
            payment.payment_status = "Pending"
            payment.razorpay_order_id = razorpay_order["id"]
            payment.save()

        return Response({
            "message": "Razorpay Order Created",
            "razorpay_order_id": razorpay_order["id"],
            "amount": razorpay_order["amount"],
            "currency": razorpay_order["currency"]
        })