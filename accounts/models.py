from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
"""Declare models for YOUR_APP app."""


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, phone_number, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        if not password:
            raise ValueError('User Must have a Password')
        if not phone_number:
            raise ValueError('User Must have a Phone Number')
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, phone_number=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, phone_number, **extra_fields)

    def create_superuser(self, email, password, phone_number, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, phone_number, **extra_fields)

class Roles(models.TextChoices):
    ADMIN = 'Admin', _('Admin')
    MANAGER = 'Manager', _('Manager')
    STAFF = 'Staff', _('Staff')

class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(
    max_length=15,
    blank=True,
    null=True
)
    role = models.CharField(max_length=50, default="Customer", choices=Roles.choices)
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='accounts_user_set',
        related_query_name='user',
        help_text=_('The groups this user belongs to.'),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='accounts_user_permissions',
        related_query_name='user',
        help_text=_('Specific permissions for this user.'),
    )
    login_otp = models.CharField(max_length=6, blank=True, null=True)
    login_otp_expiry = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'