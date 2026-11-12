from django.db import models

# Create your models here.
class Guest(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)