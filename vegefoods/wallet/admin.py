from django.contrib import admin
from . models import Wallet,WalletTransation

# Register your models here.
admin.site.register(Wallet)
admin.site.register(WalletTransation)