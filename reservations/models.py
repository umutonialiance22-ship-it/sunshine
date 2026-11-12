from django.db import models

# Create your models here.
class Reservation(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Cancelled", "Cancelled"),
    ]

    guest = models.ForeignKey(
        "guests.Guest",
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.PROTECT,
        related_name="reservations"
    )

    check_in_date = models.DateField()
    check_out_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)