from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Address,Order,OrderItem,Product
from cart_app.models import Cart,CartItem
# Create your views here.

@login_required
def place_order(request):
    user = request.user
    address = Address.objects.filter(user=user)
    cart = Cart.objects.get(user=user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    if request.method == 'POST':
        selected_address_id = request.POST.get('address')
        payment_type = request.POST.get('optradio')

        print(selected_address_id,payment_type)

         # Check if address and payment type are selected
        if not selected_address_id or not payment_type:
            # Redirect back with an error or handle it accordingly
            return render(request, 'user/checkout.html', {
                'address': address,
                'cart_items': cart_items,
                'cart': cart,
                'error_message': 'Please select an address and a payment method.'
            })

        selected_address = Address.objects.get(id=selected_address_id)
        print(selected_address)
        new_order = Order.objects.create(
            user=user,
            address=selected_address,
            payment_type=payment_type,
            total_price=cart.total_price
        )

        for item in cart_items:
            if item.product.category.category_unit == 'kg':
                price_per_kg = item.product.price
                quantity = item.quantity
                subtotal_price = price_per_kg * quantity
            elif item.product.category.category_unit == 'pack':
                price_per_pack = item.product.price
                quantity = item.quantity
                subtotal_price = price_per_pack * quantity
            else:
                # Default calculation if no specific unit
                subtotal_price = item.subtotal_price

            OrderItem.objects.create(
                order=new_order,
                product=item.product,
                quantity=item.quantity,
                price=subtotal_price / item.quantity,
                subtotal_price=subtotal_price  # Assuming this is calculated as item.quantity * item.product.price
            )
        new_order.total_price = total_price
        new_order.save()
        cart_items.delete()
        return redirect(reverse('order_success'))
    return render(request, 'user/checkout.html', {
        'address' : address,
        'cart_items': cart_items,
        'cart': cart
    })

def order_success(request):
    return render(request,'user/order_confirm.html')