from django.shortcuts import render,get_object_or_404
from product_apps.models import Product
from cart_app.models import Cart,CartItem
from django.http import JsonResponse

# Create your views here.
def cart_view(request):
    item = CartItem.objects.all()
    print(item)
    return render(request,"user/cart_app/cart.html",{'item':item})

def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        return JsonResponse({'status': 'success', 'message': 'Item added to cart'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})