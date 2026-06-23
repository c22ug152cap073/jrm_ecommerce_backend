from rest_framework import serializers
from .models import ReturnRefund


class ReturnRefundSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReturnRefund
        fields = "__all__"