from rest_framework import serializers
from .models import OrderItem


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