from rest_framework.views import APIView
from rest_framework.response import Response

from utils.email_service import (
    send_notification_email
)


class TestEmailAPIView(APIView):

    def post(self, request):

        email = request.data.get("email")

        send_notification_email(
            "Ecommerce Test Email",
            "Email notification module is working successfully.",
            email
        )

        return Response({
            "message": "Email sent successfully"
        })