from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
import random
from django.core.mail import send_mail

from .models import User
from .serializers import (
    RegisterSerializer,
    ChangePasswordSerializer,
    ResetPasswordSerializer,
)

import random
from django.utils import timezone
from datetime import timedelta
from django.utils import timezone


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class LoginAPIView(APIView):

    def post(self, request):

        print("===== LOGIN API CALLED =====")
        print("DATA:", request.data)

        email = request.data.get("email")
        password = request.data.get("password")

        print("EMAIL:", email)

        user = authenticate(
            request,
            username=email,
            password=password
        )

        print("USER:", user)

        if user is None:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })

class ProfileAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "phone_number": user.phone_number,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
        })
class ChangePasswordAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ChangePasswordSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = request.user

        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]

        if not user.check_password(old_password):
            return Response(
                {
                    "error": "Old password is incorrect"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response({
            "message": "Password changed successfully"
        })
class ForgotPasswordAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        email = request.data.get("email")

        user = User.objects.filter(
            email=email
        ).first()

        if not user:
            return Response(
                {
                    "error": "User not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        otp = str(random.randint(100000, 999999))

        user.login_otp = otp
        user.login_otp_expiry = timezone.now() + timedelta(minutes=5)
        user.save()

        return Response({
            "message": "OTP generated successfully",
            "otp": otp
        })
class VerifyOTPAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        email = request.data.get("email")
        otp = request.data.get("otp")

        user = User.objects.filter(
            email=email
        ).first()

        if not user:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if user.login_otp != otp:
            return Response(
                {"error": "Invalid OTP"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if timezone.now() > user.login_otp_expiry:
            return Response(
                {"error": "OTP expired"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            "message": "OTP verified successfully"
        })
class ResetPasswordAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = ResetPasswordSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        email = serializer.validated_data["email"]
        new_password = serializer.validated_data["new_password"]

        user = User.objects.filter(
            email=email
        ).first()

        if not user:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        user.set_password(new_password)

        user.login_otp = None
        user.login_otp_expiry = None

        user.save()

        return Response({
            "message": "Password reset successfully"
        })
