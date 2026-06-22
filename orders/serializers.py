from rest_framework import serializers
from .models import OrderItem
from .models import ShippingAddress
from .models import Payment
from .models import Invoice

class OrderItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product_name",
            "quantity",
            "price",
        ]
class ShippingAddressSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = ShippingAddress
        fields = "__all__"
class CheckoutSerializer(serializers.Serializer):
    shipping_address_id = serializers.IntegerField()

class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = "__all__"
class InvoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = "__all__"