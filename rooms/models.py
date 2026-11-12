from django.db import models

# Create your models here.
class Room(models.Model):
    room_number = models.CharField(max_length=3, unique=True)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_occupancy = models.PositiveIntegerField()

    def __str__(self):
        return self.room_number