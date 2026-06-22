from django.db import models


class Banner(models.Model):

    title = models.CharField(
        max_length=255
    )

    subtitle = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    banner_image = models.ImageField(
        upload_to="banners/"
    )

    button_text = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    button_link = models.URLField(
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title