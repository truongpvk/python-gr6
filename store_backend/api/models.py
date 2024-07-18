from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=0)
    quantity = models.PositiveIntegerField()
    quantity_sold = models.PositiveIntegerField(default=0)