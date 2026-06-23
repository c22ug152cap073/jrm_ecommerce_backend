from django.db import models
from orders.models import Order


class ReturnRefund(models.Model):

    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Refunded", "Refunded"),
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Return #{self.id}"