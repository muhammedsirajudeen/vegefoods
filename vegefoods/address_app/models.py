from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Address(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE,related_name='addresses')
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    alternative_phone_number = models.CharField(max_length=255)
    pincode = models.CharField(max_length=255)
    locality =  models.CharField(max_length=255)
    landmark =  models.CharField(max_length=255,blank=True,null=True)
    district =  models.CharField(max_length=255)
    state =  models.CharField(max_length=255)
    country  =  models.CharField(max_length=255)
    address = models.TextField()
    ADDRESS_TYPE_CHOICES = [
        ('H','Home'),
        ('O','Office'),
        ('OT','Other')
    ]
    address_type = models.CharField(max_length=12,choices=ADDRESS_TYPE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.name} - {self.get_address_type_display()}"
