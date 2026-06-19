from rest_framework import serializers
from .models import OrderItem
from .models import ShippingAddress

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