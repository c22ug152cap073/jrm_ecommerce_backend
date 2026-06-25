from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import ReturnRefund
from .serializers import ReturnRefundSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.email_service import send_notification_email
from orders.models import OrderItem



class ReturnRefundListCreateAPIView(
    generics.ListCreateAPIView
):

    queryset = ReturnRefund.objects.all()

    serializer_class = ReturnRefundSerializer

    permission_classes = [AllowAny]

    def perform_create(self, serializer):

        return_request = serializer.save()

        send_notification_email(
            "Return Request Submitted",
            f"Your return request for Order #{return_request.order.id} has been received.",
            return_request.order.user.email
        )

class UpdateReturnStatusAPIView(APIView):

    def put(self, request, return_id):

        status_value = request.data.get("status")

        return_request = ReturnRefund.objects.filter(
            id=return_id
        ).first()

        if not return_request:
            return Response(
                {"error": "Return request not found"},
                status=404
            )

        return_request.status = status_value
        return_request.save()

        if status_value == "Approved":
            order_items = OrderItem.objects.filter(
                order=return_request.order
            )

            for item in order_items:
                item.product.stock += item.quantity
                item.product.save()

            send_notification_email(
                "Refund Approved",
                f"Your refund request for Order #{return_request.order.id} has been approved.",
                return_request.order.user.email
            )

        return Response({
            "message": "Return status updated",
            "status": return_request.status
        })
class ReturnHistoryAPIView(
    generics.ListAPIView
):

    serializer_class = ReturnRefundSerializer

    def get_queryset(self):

        order_id = self.request.GET.get("order_id")

        if order_id:
            return ReturnRefund.objects.filter(
                order_id=order_id
            ).order_by("-created_at")

        return ReturnRefund.objects.all().order_by(
    "-created_at"
)