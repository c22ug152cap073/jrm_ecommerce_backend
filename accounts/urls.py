from django.urls import path
from .views import (
    RegisterAPIView,
    LoginAPIView,
    ProfileAPIView,
    ChangePasswordAPIView,
    ForgotPasswordAPIView,
    VerifyOTPAPIView,
    ResetPasswordAPIView,
)

urlpatterns = [
    path("register/", RegisterAPIView.as_view()),
    path("login/", LoginAPIView.as_view()),
    path("profile/", ProfileAPIView.as_view()),
    path("change-password/", ChangePasswordAPIView.as_view()),
    path("forgot-password/", ForgotPasswordAPIView.as_view()),
    path("verify-otp/", VerifyOTPAPIView.as_view()),
    path("reset-password/", ResetPasswordAPIView.as_view()),
    
]