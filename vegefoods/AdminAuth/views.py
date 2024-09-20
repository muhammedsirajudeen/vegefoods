from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.db.models import Sum,Count,Q
from order_app.models import Order,OrderItem
from category_app.models import Category
from django.db.models.functions import ExtractMonth
from django.http import JsonResponse


def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('panel') 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:  
            login(request, user)
            return redirect('panel')  
        else:
            return render(request, 'admin/admin_login.html', {'error': 'Invalid credentials or access denied'})
    return render(request, 'admin/admin_login.html')

def panel(request):
    if not request.user.is_authenticated or not request.user.is_superuser: 
        return redirect('admin_login')
    total_sales = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
    sales_count = Order.objects.count()
    top_products = OrderItem.objects.values(
    'product__product_name', 
    'product__image_1', 
    'product__available_stock',
    'product__category__category_unit'
    ).annotate(
    total_quantity_sold=Sum('quantity'), 
    total_revenue=Sum('subtotal_price'),

    ).order_by('-total_quantity_sold')[:10]

    orders_by_pincode = Order.objects.values(
        'user__addresses__pincode',
        'user__addresses__state',
        'user__addresses__district'
    ).annotate(
        total_orders=Count('id')
    ).order_by('-total_orders')
    top_customers = (
        User.objects
        .filter(is_superuser=False)
        .annotate(total_orders= Count('order'))
        .annotate(total_spend=Sum('order__total_price'))
        .filter(total_orders__gt=0) 
        .order_by('-total_spend')[:10]
    )
    
    top_category = OrderItem.objects.values(
        'product__category__category_name',
        'product__category__category_unit',
    ).annotate(
        total_quantity_sold = Sum('quantity'),
        total_revenue=Sum('subtotal_price'),
    ).order_by('-total_quantity_sold')[:10]

    top_categories = OrderItem.objects.values('product__category__category_name').annotate(
        total_quantity_sold=Sum('quantity')
    ).order_by('-total_quantity_sold')[:5]  # Limit to top 5 categories
    
    categories = [category['product__category__category_name'] for category in top_categories]
    quantities = [category['total_quantity_sold'] for category in top_categories]

    context={
        'total_sales':total_sales,
        'sales_count':sales_count,
        'top_products':top_products,
        'orders_by_pincode': orders_by_pincode,
        'top_customers':top_customers,
        'top_category':top_category, 
        'categories': categories,
        'quantities': quantities,
    }
    return render(request, 'admin/dashboard.html',context)  

 
def user_managment(request): 
    if not request.user.is_authenticated or not request.user.is_superuser:  
        return redirect('admin_login') 
    users = User.objects.filter(is_superuser =  False).order_by('username')
    return render(request,'admin/users.html',{'users':users})


def block_unblock_user(request, user_id):
    if not request.user.is_authenticated or not request.user.is_superuser:  
        return redirect('admin_login') 

    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'block':
            user.is_active = False
        elif action == 'unblock':
            user.is_active = True
        user.save()

    return redirect('user_management')  

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

def ledger_book_view(request):
    # Fetch all orders along with their associated items
    total_sales_price = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_sales_delivered = OrderItem.objects.filter(status='Delivered').aggregate(
        total=Sum('subtotal_price'))['total'] or 0

    total_refunds = OrderItem.objects.filter(
    Q(status='Cancelled') | Q(status='Approve Returned')
    ).aggregate(refunded_amount=Sum('subtotal_price'))['refunded_amount'] or 0

    total_orders = Order.objects.count()
    total_orders_delivered = Order.objects.filter(items__status='Delivered').count()

    total_canceled_items =OrderItem.objects.filter(status='Cancelled').count()
    total_returned_items = OrderItem.objects.filter(status='Approve Returned').count()
    
    total_products_ordered =  OrderItem.objects.values('product').count()

    total_products_in_progress = OrderItem.objects.filter(
        Q(status='Order Pending') | 
        Q(status='Order confirmed') | 
        Q(status='Shipped') | 
        Q(status='Out For Delivery')
    ).count()

    context = {
        'total_sales_price': total_sales_price,
        'total_sales_delivered':total_sales_delivered,
        'total_refunds':total_refunds,
        'total_orders':total_orders,
        'total_orders_delivered':total_orders_delivered,
        'total_canceled_items':total_canceled_items,
        'total_returned_items':total_returned_items,
        'total_products_ordered':total_products_ordered,
        'total_products_in_progress': total_products_in_progress

    }
    
    return render(request, 'admin/ledger_book.html', context)



def get_monthly_orders(request, year):
    # Query to count orders by month
    orders = Order.objects.filter(created_at__year=year).annotate(
        month=ExtractMonth('created_at')
    ).values('month').annotate(count=Count('id')).order_by('month')
    
    # Prepare data for each month
    monthly_data = [0] * 12
    for order in orders:
        monthly_data[order['month'] - 1] = order['count']

    return JsonResponse({
        'labels': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        'data': monthly_data
    })

