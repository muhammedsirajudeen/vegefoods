from django.db import models
from  django.contrib.auth.models import User
# Create your models here.
class Wallet(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    balance =  models.DecimalField(max_digits=10,decimal_places=2,default=0.00)

class WalletTransation(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('refund', 'Refund'),
        ('cancellation', 'Cancellation'),
    ]

    wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20,choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    created_at =  models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username}'s Wallet - Balance: {self.balance}"

    def __str__(self):
        return f"{self.wallet.user.username} - {self.transaction_type} - {self.amount}"