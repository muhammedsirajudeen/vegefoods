from django.shortcuts import render,redirect,get_object_or_404
from . models import Product
from category_app.models import Category
from django.contrib.auth.models import User
from . forms import ProductForm
from django.db.models import  F
from django.contrib import messages
# Create your views here.



def product_list(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admin_login')  #
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully.')
            return redirect('product_management')  # Adjust as necessary
        else:
            # Collect form errors for display
            errors = form.errors
    else:
        form = ProductForm()
        errors = None

    product = Product.objects.all()
    categories = Category.objects.all()
    
    return render(request, 'admin/product.html', {
        'form': form,
        'product': product,
        'categories': categories,
        'errors': errors,
    })


# View to edit an existing product
def edit_product(request, product_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admin_login') 
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # Extract data from the form
        product_name = request.POST.get('product_name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        available_stock = request.POST.get('available_stock')
        price = request.POST.get('price')
        offer = request.POST.get('offer')
        
        # Handle file uploads
        image_1 = request.FILES.get('image_1')
        image_2 = request.FILES.get('image_2')
        image_3 = request.FILES.get('image_3')

        # Update the product object
        product.product_name = product_name
        product.description = description
        product.category_id = category_id
        product.available_stock = available_stock
        product.price = price
        product.offer = offer

        # Update images if files are provided
        if image_1:
            product.image_1 = image_1
        if image_2:
            product.image_2 = image_2
        if image_3:
            product.image_3 = image_3
        
        # Save the changes to the database
        product.save()

        # Redirect to the product management page or any other page
        return redirect('product_management')

    else:
        # Render the form with i
        return render(request, 'admin/edit_product.html', {
            'product': product,
            'categories': Category.objects.all(),  # Assuming you have a Category model
        })


  
def toggle_product_listing(request, product_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admin_login') 
    print(f"Toggling listing for product_id: {product_id}")
    product = get_object_or_404(Product, id=product_id)
    product.is_listed = not product.is_listed
    product.save()
    return redirect('product_management')




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