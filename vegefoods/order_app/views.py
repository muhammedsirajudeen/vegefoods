from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Address, Order, OrderItem, Product
from cart_app.models import Cart, CartItem
from decimal import Decimal  

@login_required
def place_order(request):
    user = request.user
    address = Address.objects.filter(user=user)
    cart = Cart.objects.get(user=user)
    cart_items = CartItem.objects.filter(cart=cart)

    
    subtotal_price = Decimal('0.00')
    cart_items_with_subtotals = []

    
    for item in cart_items:
        quantity = Decimal(item.quantity)
        if item.product.category.category_unit == 'kg':
            item_price = item.product.price * quantity
        elif item.product.category.category_unit == 'pack':
            item_price = item.product.price * quantity
        else:
            item_price = item.product.price * quantity

        subtotal_price += item_price
        cart_items_with_subtotals.append({
            'item': item,
            'item_subtotal': item_price
        })

    delivery_charge = Decimal('40.00') if subtotal_price <= Decimal('200.00') else Decimal('0.00')

    
    total_price = subtotal_price + delivery_charge

    if request.method == 'POST':
        selected_address_id = request.POST.get('address')
        payment_type = request.POST.get('optradio')

        if not selected_address_id or not payment_type:
            return render(request, 'user/checkout.html', {
                'address': address,
                'cart_items': cart_items_with_subtotals,
                'cart': cart,
                'subtotal_price': subtotal_price,
                'delivery_charge': delivery_charge,
                'total_price': total_price,
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
            quantity = Decimal(item.quantity)
            if item.product.category.category_unit == 'kg':
                subtotal_price = item.product.price * quantity
            elif item.product.category.category_unit == 'pack':
                subtotal_price = item.product.price * quantity
            else:
                subtotal_price = item.product.price * quantity

            OrderItem.objects.create(
                order=new_order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
                subtotal_price=subtotal_price
            )
            product = item.product
            product.available_stock -= item.quantity
            product.save()
            
        cart_items.delete()
        return redirect(reverse('order_success'))

    return render(request, 'user/checkout.html', {
        'address': address,
        'cart_items': cart_items_with_subtotals,  
        'cart': cart,
        'subtotal_price': subtotal_price,
        'delivery_charge': delivery_charge,
        'total_price': total_price
    })
@login_required
def order_success(request):
    return render(request,'user/order_confirm.html')


@login_required
def user_order_list(request):

    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')  
   
    order_items = OrderItem.objects.filter(order__in=orders)  

    return render(request, 'user/user_order/orderlist.html', {'order_items': order_items})

def admin_order_list(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admin_login') 
    orders = Order.objects.all()
    return render(request,'admin/order_admin.html',{'order':orders})


def admin_order_details(request, order_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admin_login') 

    order = get_object_or_404(Order, id=order_id)
    order_items = order.items.all()
    
    context = {
        'order': order,
        'order_items': order_items
    }
    return render(request, 'admin/order_details_admin.html', context)


def edit_checkout_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)  
    if request.method == 'POST':
        address.name = request.POST.get("name")
        address.phone_number = request.POST.get("phone")
        address.alternative_phone_number = request.POST.get("alt_phone")
        address.pincode = request.POST.get("pincode")
        address.locality = request.POST.get("locality")
        address.landmark = request.POST.get("landmark")
        address.district = request.POST.get("district")
        address.state = request.POST.get("state")
        address.country = request.POST.get("country")
        address.address = request.POST.get("address")
        address.address_type= request.POST.get("addressType")
        address.save()
        
        return redirect('place_order')  # Redirect to address list page after saving

    return render(request,"user/address_app/edit_checkout_address.html",{'address': address})

def add_address_checkout(request):
    
     
    if request.method == 'POST':
 
        name  =  request.POST.get("name")
        phone_number= request.POST.get("phone")
        alternative_phone = request.POST.get("alt_phone")
        pincode = request.POST.get("pincode")
        locality = request.POST.get("locality")
        landmark = request.POST.get("landmark")
        district = request.POST.get("district")
        state = request.POST.get("state")
        country = request.POST.get("country")
        address = request.POST.get("address")
        address_type = request.POST.get("addressType")

        Address.objects.create(
            user = request.user,
            name =name,
            phone_number = phone_number,
            alternative_phone_number =  alternative_phone,
            pincode = pincode,
            locality =  locality,
            landmark = landmark,
            district =  district,
            state = state,
            country = country,
            address = address,
            address_type = address_type
        )
        return redirect('place_order')  # Redirect to address list page after saving

    return render(request, "user/address_app/add_addresscheckout.html")




def user_order_details(request):
    return render(request,"user/orderdetails.html")

def update_order_status(request,order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        # Iterate through each order item to update status
        for item in order.items.all():
            new_status = request.POST.get(f'status_{item.id}')
            print(new_status)
            if new_status:
                item.status = new_status
                item.save()
        
        return redirect('order-managment')  # Redirect to the admin order list

    # If GET request, redirect to order details or some other page
    return redirect('admin_order_details', order_id=order_id)
