from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random

class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return self.created_at >= timezone.now() - timedelta(minutes=10)

    def save(self, *args, **kwargs):
        if not self.otp_code:
            self.otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} - {self.otp_code}'


class Message(models.Model):
    STATUS = [
        ('pending', 'Pending'),
        ('solved', 'Solved')
    ]
    name = models.CharField(max_length=100)  # Increased length for names
    email = models.EmailField(max_length=100)  # Changed to EmailField with increased length
    phone_number = models.CharField(max_length=14)  # This is fine as is, but validate formats
    subject = models.CharField(max_length=100)  # Increased length for subjects
    message = models.TextField()  # Use TextField for longer messages
    status = models.CharField(max_length=20, choices=STATUS, default='pending')  # Default status
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} complaint: {self.subject}"
    


