from django.db import models
from cloudinary.models import CloudinaryField

class Category(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('packet', 'Packet'),
    ]

    category_name = models.CharField(max_length=255)
    category_image = CloudinaryField('image', blank=True, null=True)
    category_offer = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    is_listed = models.BooleanField(default=True)
    category_unit = models.CharField(max_length=50, choices=UNIT_CHOICES, blank=True, null=True)  # e.g., kg, packet, etc.
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.category_name
