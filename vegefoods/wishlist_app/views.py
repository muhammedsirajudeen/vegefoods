from django.shortcuts import render,get_object_or_404,redirect
from product_apps.models import Product
from wishlist_app.models import Wishlist
from django.contrib import messages 
# Create your views here.
def view_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request,'user/cart_app/wishlist.html',{'wishlist_items':wishlist_items})


def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    
    if created:
        messages.success(request, f"{product.product_name} has been added to your wishlist.")
    else:
        messages.info(request, f"{product.product_name} is already in your wishlist.")
    
   
    return redirect('view_wishlist')


def remove_wishlist(request,product_id):
    product =  get_object_or_404(Product,id=product_id)
    wishlist_item = Wishlist.objects.filter(user=request.user,product=product).first()

    if wishlist_item:
        wishlist_item.delete()
        messages.success(request, f"{product.product_name} has been removed from your wishlist.")
    else:
        messages.error(request, "This item is not in your wishlist.")
    
    return redirect('view_wishlist')
        