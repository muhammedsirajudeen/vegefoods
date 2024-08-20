from django.shortcuts import render,redirect,get_object_or_404
from . models import Product
from category_app.models import Category
from . forms import ProductForm

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


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_management')
    else:
        form = ProductForm(instance=product)

    categories = Category.objects.all()

    return render(request, 'admin/product.html', {
        'form': form,
        'products': Product.objects.all(),
        'categories': categories,
        'editing_product': product
    })
