from django.shortcuts import render,get_object_or_404
from . models import Wallet,WalletTransation
from  django.contrib.auth.models import User

# Create your views here.
def wallet_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # Get or create the wallet for the user
    wallet, created = Wallet.objects.get_or_create(user=user, defaults={'balance': 0.00})

    # Fetch the filter parameter from the request
    filter_type = request.GET.get('filter', 'all').lower()
    
    # Filter the wallet transactions based on the filter_type
    if filter_type == 'debited':
        wallet_details = WalletTransation.objects.filter(wallet=wallet, transaction_type='Debited').order_by('-created_at')
    elif filter_type == 'refund':
        wallet_details = WalletTransation.objects.filter(wallet=wallet, transaction_type='refund').order_by('-created_at')
    elif filter_type == 'cancellation':
        wallet_details = WalletTransation.objects.filter(wallet=wallet, transaction_type='cancellation').order_by('-created_at')
    else:  # Default case: show all transactions
        wallet_details = WalletTransation.objects.filter(wallet=wallet).order_by('-created_at')



    # Pass the wallet and its transactions to the context
    context = {
        'wallet': wallet,
        'wallet_details': wallet_details,
        'selected_filter': filter_type
    }

    return render(request, 'user/wallet/wallet.html', context)