from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Address, Order, OrderItem, Product,Invoice
from cart_app.models import Cart, CartItem
from decimal import Decimal  
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import random
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# Razorpay client initialization
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


@login_required
def place_order(request):
    user = request.user
    address = Address.objects.filter(user=user)
    cart = Cart.objects.get(user=user)
    cart_items = CartItem.objects.filter(cart=cart)

    subtotal_price = Decimal('0.00')
    cart_items_with_subtotals = []

    # Calculating the item prices based on quantity and category unit
    for item in cart_items:
        quantity = Decimal(item.quantity)
        if item.product.category.category_unit == 'kg':
            item_price = Decimal(item.product.price) * quantity
        elif item.product.category.category_unit == 'pack':
            item_price = Decimal(item.product.price) * quantity
        else:
            item_price = Decimal(item.product.price) * quantity

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

        if payment_type == 'Razor pay':
            # Create Razorpay order
            request.session['selected_address'] = selected_address_id

            razorpay_order = razorpay_client.order.create({
                'amount': int(Decimal(total_price) * Decimal('100')),  # amount in paisa
                'currency': 'INR',
                'payment_capture': '1'
            })

            return render(request, 'user/razorpay/razorpay_payment.html', {
                'razorpay_order_id': razorpay_order['id'],
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                'amount': total_price,
                'selected_address': selected_address,
            })

        # Handle Cash on Delivery
        if payment_type == 'Cash on Delivery' and total_price > Decimal('1000.00'):
            print("not cod")
            return render(request, 'user/checkout.html', {
                'address': address,
                'cart_items': cart_items_with_subtotals,
                'cart': cart,
                'subtotal_price': subtotal_price,
                'delivery_charge': delivery_charge,
                'total_price': total_price,
                'error_message': 'Cash on Delivery is not available for orders above ₹1000.'
            })

        new_order = Order.objects.create(
            user=user,
            address=selected_address,
            payment_type=payment_type,
            total_price=total_price
        )

        for item in cart_items:
            quantity = Decimal(item.quantity)
            if item.product.category.category_unit == 'kg':
                item_price = Decimal(item.product.price) * quantity
            elif item.product.category.category_unit == 'pack':
                item_price = Decimal(item.product.price) * quantity
            else:
                item_price = Decimal(item.product.price) * quantity

            OrderItem.objects.create(
                order=new_order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
                subtotal_price=item_price
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


@csrf_exempt
def razorpay_payment_status(request):
    if request.method == "POST":
        payment_id = request.POST.get("razorpay_payment_id")
        razorpay_order_id = request.POST.get("razorpay_order_id")
        razorpay_signature = request.POST.get("razorpay_signature")

        try:
            # Verify the Razorpay payment signature
            razorpay_client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': razorpay_signature
            })

            # Payment is successful, proceed with creating the order
            user = request.user
            cart = Cart.objects.get(user=user)
            cart_items = CartItem.objects.filter(cart=cart)
            selected_address_id = request.session.get('selected_address')
            selected_address = Address.objects.get(id=selected_address_id)

            # Create the order
            new_order = Order.objects.create(
                user=user,
                address=selected_address,
                payment_type='Razor pay',
                total_price=sum([Decimal(item.product.price) * Decimal(item.quantity) for item in cart_items])
            )

            # Create order items and reduce stock
            for item in cart_items:
                quantity = Decimal(item.quantity)
                if item.product.category.category_unit == 'kg':
                    item_price = Decimal(item.product.price) * quantity
                elif item.product.category.category_unit == 'pack':
                    item_price = Decimal(item.product.price) * quantity
                else:
                    item_price = Decimal(item.product.price) * quantity

                OrderItem.objects.create(
                    order=new_order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                    subtotal_price=item_price
                )
                item.product.available_stock -= item.quantity
                item.product.save()

            # Clear the cart after order creation
            cart_items.delete()
            return redirect('order_success')

        except razorpay.errors.SignatureVerificationError:
            # Handle verification failure
            return render(request, 'user/order_confirm.html', {
                'error_message': 'Payment verification failed. Please try again.'
            })

    return redirect('order_success')
@login_required
def order_success(request):
    return render(request,'user/order_confirm.html')


@login_required
def user_order_list(request):

    user = request.user
    
    orders = Order.objects.filter(user=user).order_by('-created_at')
    # Get the IDs of the most recent orders
    order_ids = orders.values_list('id', flat=True)
    # Fetch order items related to these orders, ordered by their creation time
    order_items = OrderItem.objects.filter(order__in=order_ids).order_by('-order__created_at')


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


def user_order_details(request,order_id):
    order_items = get_object_or_404(OrderItem, id=order_id)
    order = order_items.order
    context = {
       
        'order_items': order_items,
        'order' : order
    }
    return render(request,"user/orderdetails.html",context)



def generate_invoice_number():
    """Generate a unique invoice number with pattern 'vege123123XXX'."""
    unique_id = random.randint(100000, 999999)  # Generate random 6-digit number
    return f"vege{unique_id}"

def download_invoice_item(request, item_id):
    order_item = OrderItem.objects.get(id=item_id)

    order = order_item.order

    # Get or create an invoice for the order item
    invoice, created = Invoice.objects.get_or_create(order_item=order_item)

    if created:
        invoice.invoice_number = generate_invoice_number()
        invoice.save()

    # Generate the HTML string for the invoice (whether newly created or not)
    html_string = render_to_string('user/user_invoice/invoice.html', {
        'order_item': order_item,
        'invoice_number': invoice.invoice_number,
        'invoice_date': invoice.invoice_date,
        'order': order,
    })

    # Create a PDF file from the HTML string
    pdf = HTML(string=html_string).write_pdf()

    # Create the HTTP response to download the PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_item_{order_item.id}.pdf"'

    return response
