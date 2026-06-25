from django.db import models
from django.conf import settings
from products.models import Product


class RecentlyViewed(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    viewed_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-viewed_at"]
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user.email} - {self.product.name}"