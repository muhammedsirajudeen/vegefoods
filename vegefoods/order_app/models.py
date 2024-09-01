from django.db import models
from django.contrib.auth.models import User
from product_apps.models import Product
from address_app.models import Address 
import uuid

# Create your models here.
class Order(models.Model):
    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('RazorPay', 'Razor Pay'),
        ('UPI', 'UPI')
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Return', 'Return')
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    estimated_delivery_date = models.DateField(blank=True, null=True)
    coupon_code = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'
    

    def generate_order_number(self):
        return f'{uuid.uuid4().hex[:6].upper()}-{timezone.now().strftime("%Y%m%d%H%M%S")}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


    def __str__(self):
        return f'{self.quantity} of {self.product.product_name} in order {self.order.id}'
