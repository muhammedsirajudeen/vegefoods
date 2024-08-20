from django.db import models
from cloudinary.models import CloudinaryField
from category_app.models import Category  

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=255)
    description  = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  
    available_stock = models.PositiveIntegerField()
    image_1 = CloudinaryField('image')
    image_2 = CloudinaryField('image', blank=True, null=True)
    image_3 = CloudinaryField('image', blank=True, null=True)
    offer = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_listed = models.BooleanField(default=True)

    def __str__(self):
        return self.product_name
