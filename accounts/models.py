from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)

class Roles(models.TextChoices):
    ADMIN = 'Admin', _('Admin')
    MANAGER = 'Manager', _('Manager')
    STAFF = 'Staff', _('Staff')

class User(AbstractUser):
    username = models.CharField(
    max_length=150,
    blank=True,
    null=True
)

    email = models.EmailField(
        unique=True
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        related_name='accounts_user_permissions',
        related_query_name='user',
        help_text=_('Specific permissions for this user.'),
    )
    login_otp = models.CharField(max_length=6, blank=True, null=True)
    login_otp_expiry = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return self.email