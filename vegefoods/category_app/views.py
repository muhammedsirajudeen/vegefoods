from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from .models import Category
from .forms import CategoryForm
from django.contrib import messages


def category_management(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admin_login') 
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect(reverse('category_management'))
        else:
           
            errors = form.errors

    else:
        errors = None

    categories = Category.objects.all()

    return render(request, 'admin/category.html', {
        'categories': categories,
        'form': form,
        'errors': errors  
    })


def edit_category(request, category_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admin_login') 
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category_image = request.FILES.get('category_image')
        category_offer = request.POST.get('category_offer')
        category_unit = request.POST.get('category_unit')

        errors = {}

       
        if Category.objects.exclude(id=category_id).filter(category_name__iexact=category_name).exists():
            errors['category_name'] = 'Category name already exists'
        if not category_name.isalpha():
            errors['category_name'] = 'Category name must contain characters only'


        if not category_unit.isalpha():
            errors['category_unit'] = 'Category unit must contain characters only'

        if errors:
            return render(request, 'admin/edit_category.html', {
                'category': category,
                'errors': errors
            })

        
        category_name = category_name.title()  
        category_unit = category_unit.lower() 

       
        category.category_name = category_name
        category.category_offer = category_offer
        category.category_unit = category_unit
        if category_image:
            category.category_image = category_image
        category.save()

        messages.success(request, 'Category updated successfully.')
        return redirect('category_management')

    return render(request, 'admin/edit_category.html', {
        'category': category
    })

def toggle_category_listing(request, category_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admin_login') 
    category=  get_object_or_404(Category,id = category_id)
    category.is_listed = not category.is_listed
    category.save()
    return redirect('category_management')