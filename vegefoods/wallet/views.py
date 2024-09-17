from django.shortcuts import render,get_object_or_404
from . models import Wallet,WalletTransation
from  django.contrib.auth.models import User

# Create your views here.
def wallet_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # Get or create the wallet for the user
    wallet, created = Wallet.objects.get_or_create(user=user, defaults={'balance': 0.00})

    # Fetch wallet transactions
    wallet_details = WalletTransation.objects.filter(wallet=wallet)

    # Pass the wallet and its transactions to the context
    context = {
        'wallet': wallet,
        'wallet_details': wallet_details
    }

    return render(request, 'user/wallet/wallet.html', context)