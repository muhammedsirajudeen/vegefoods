from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Address, Order, OrderItem, Product
from cart_app.models import Cart, CartItem
from decimal import Decimal  # Import Decimal

@login_required
def place_order(request):
    user = request.user
    address = Address.objects.filter(user=user)
    cart = Cart.objects.get(user=user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    # Calculate the total price
    total_price = Decimal('0.00')
    for item in cart_items:
        # Convert quantity to Decimal to avoid type errors
        quantity = Decimal(item.quantity)
        
        if item.product.category.category_unit == 'kg':
            price_per_kg = item.product.price  # Assuming this is already a DecimalField
            subtotal_price = price_per_kg * quantity
        elif item.product.category.category_unit == 'pack':
            price_per_pack = item.product.price  # Assuming this is already a DecimalField
            subtotal_price = price_per_pack * quantity
        else:
            # Handle cases where the unit is neither 'kg' nor 'pack'
            subtotal_price = item.product.price * quantity

        total_price += subtotal_price

    # Add delivery charge based on subtotal
    delivery_charge = Decimal('40.00') if total_price <= Decimal('200.00') else Decimal('0.00')
    total_price += delivery_charge

    if request.method == 'POST':
        selected_address_id = request.POST.get('address')
        payment_type = request.POST.get('optradio')

        if not selected_address_id or not payment_type:
            return render(request, 'user/checkout.html', {
                'address': address,
                'cart_items': cart_items,
                'cart': cart,
                'total_price': total_price,  # Pass the total price to the template
                'error_message': 'Please select an address and a payment method.'
            })

        selected_address = Address.objects.get(id=selected_address_id)
        new_order = Order.objects.create(
            user=user,
            address=selected_address,
            payment_type=payment_type,
            total_price=total_price
        )

        for item in cart_items:
            # Ensure price calculation uses Decimal
            if item.product.category.category_unit == 'kg':
                price_per_kg = item.product.price
                quantity = Decimal(item.quantity)
                subtotal_price = price_per_kg * quantity
            elif item.product.category.category_unit == 'pack':
                price_per_pack = item.product.price
                quantity = Decimal(item.quantity)
                subtotal_price = price_per_pack * quantity
            else:
                subtotal_price = item.product.price * Decimal(item.quantity)

            OrderItem.objects.create(
                order=new_order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,  # Price per unit
                subtotal_price=subtotal_price
            )

        cart_items.delete()
        return redirect(reverse('order_success'))

    return render(request, 'user/checkout.html', {
        'address': address,
        'cart_items': cart_items,
        'cart': cart,
        'total_price': total_price  # Pass the total price to the template
    })

@login_required
def order_success(request):
    return render(request,'user/order_confirm.html')


@login_required
def user_order_details(request):

    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')  # Fetch orders for the logged-in user
   
    order_items = OrderItem.objects.filter(order__in=orders)  # Fetch order items for those orders

    return render(request, 'user/user_order/orderlist.html', {'order_items': order_items})

def admin_order_list(request):
    orders = Order.objects.all()
    return render(request,'admin/order_admin.html',{'order':orders})


def admin_order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # Retrieve related order items via the related name defined in OrderItem
    order_items = order.items.all()
    
    context = {
        'order': order,
        'order_items': order_items
    }
    return render(request, 'admin/order_details_admin.html', context)