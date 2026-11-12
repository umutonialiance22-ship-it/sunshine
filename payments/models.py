from django.db import models

# Create your models here.
class Payment(models.Model):

    STATUS_CHOICES = [
        ("Success", "Success"),
        ("Failed", "Failed"),
    ]

    reservation = models.OneToOneField(
        "reservations.Reservation",
        on_delete=models.CASCADE,
        related_name="payment"
    )

    transaction_ref = models.CharField(
        max_length=255,
        unique=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )

    created_at = models.DateTimeField(auto_now_add=True)