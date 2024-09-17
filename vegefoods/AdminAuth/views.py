from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.db.models import Sum,Count
from order_app.models import Order,OrderItem

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
    for i in top_products:
        print("top products",i)

    context={
        'total_sales':total_sales,
        'sales_count':sales_count,
        'top_products':top_products,
        'orders_by_pincode': orders_by_pincode,
        'top_customers':top_customers
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

