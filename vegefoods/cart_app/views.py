from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from .models import Product, CartItem,Cart
from django.views.decorators.csrf import csrf_exempt

def cart_view(request):
    if request.user.is_authenticated:

        cart, created = Cart.objects.get_or_create(user=request.user)
        user_cart = cart.items.all()
        context = {
            'items': user_cart,
        }
    else:
        context = {
            'items': [],
        }
    return render(request, 'user/cart_app/cart.html', context)


def add_to_cart(request):
    if request.method == 'POST' and request.user.is_authenticated:
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity', 1)
        product = get_object_or_404(Product, id=product_id)

        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Check if the item is already in the cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += int(quantity)  # If it exists, update the quantity
        else:
            cart_item.quantity = int(quantity)  # If it's a new item, set the quantity

        cart_item.save()

        return JsonResponse({'success': True, 'message': 'Item added to cart'})
    
    return JsonResponse({'success': False, 'message': 'User not authenticated or invalid request'})

                