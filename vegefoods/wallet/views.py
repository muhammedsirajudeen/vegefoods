from django.shortcuts import render,get_object_or_404
from . models import Wallet,WalletTransation
from  django.contrib.auth.models import User

# Create your views here.
def wallet_view(request,user_id):
    user =  get_object_or_404(User,id=user_id)
    wallet = get_object_or_404(Wallet,user=user)
    wallet_details = WalletTransation.objects.filter(wallet=wallet)
    context= {
        'wallet':wallet,
        'wallet_details':wallet_details
    }
    return render(request,'user/wallet/wallet.html',context)


