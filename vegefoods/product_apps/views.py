from django.shortcuts import render,redirect,get_object_or_404
from . models import Product
from category_app.models import Category
from django.contrib.auth.models import User
from . forms import ProductForm
from django.db.models import  F
# Create your views here.


def product_list(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_management')  # Adjust as necessary
    else:
        form = ProductForm()

    product = Product.objects.all()
    categories = Category.objects.all()
    
    return render(request, 'admin/product.html', {
        'form': form,
        'product': product,
        'categories': categories
    })


# View to edit an existing product
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_management')  # Redirect to product management page after saving
    else:
        form = ProductForm(instance=product)

    products = Product.objects.all()
    categories = Category.objects.all()

    return render(request, 'admin/edit_product.html', {
        'form': form,
        'products': products,
        'categories': categories,
        'editing_product': product,  # Ensure you use 'editing_product' to match the template variable
    })
  


def user_products(request):
    username = request.user.username
    category = request.GET.get('category', 'All') 
    sort_by = request.GET.get('sort_by','default') 

    if category == 'All':
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(category__category_name=category) 

    if sort_by == 'price_low_high':
        product_list = product_list.order_by('price')
    elif sort_by == 'price_high_low':
        product_list = product_list.order_by('-price')
    elif sort_by == 'discount':
        product_list = product_list.order_by('-offer')
    else:
        pass
    return render(request, 'user/shop.html', {
        'products': product_list,
        'username': username,
        'selected_category': category,
        'selected_sort':sort_by,
    })


def product_details(request,product_id):
    product = get_object_or_404(Product,id=product_id)
    username = request.user.username
    return render(request,'user/product-single.html', {'product':product,'username': username})