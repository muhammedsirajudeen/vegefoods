from django.db import models
from django.contrib.auth.models import User
from product_apps.models import Product
from address_app.models import Address 
import uuid
from django.utils import timezone 
from datetime import timedelta 

class Order(models.Model):
    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('RazorPay', 'Razor Pay'),
        ('UPI', 'UPI')
    ]
   
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    estimated_delivery_date = models.DateField(blank=True, null=True)
    coupon_code = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

    def save(self, *args, **kwargs):
        # Generate order number if it doesn't exist
        if not self.order_number:
            self.order_number = str(uuid.uuid4().hex[:8])

        # Set estimated delivery date to 6 days from the current date if not already set
        if not self.estimated_delivery_date:
            self.estimated_delivery_date = timezone.now().date() + timedelta(days=6)

        super().save(*args, **kwargs)

class OrderItem(models.Model):
    STATUS_CHOICES = [
        ("Order Pending", "Order Pending"),
        ("Order confirmed", "Order confirmed"),
        ("Shipped", "Shipped"),
        ("Out For Delivery", "Out For Delivery"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
        ("Requested Return","Requested Return"),
        ("Approve Returned", "Approve Returned"),
        ("Reject Returned", "Reject Returned"),

    ]
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Order Pending') 
    subtotal_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    return_reason = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.quantity} of {self.product.product_name} in order {self.order.id}'



class Invoice(models.Model):
    order_item = models.OneToOneField(OrderItem,on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=50,unique=True)
    invoice_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.invoice_number

