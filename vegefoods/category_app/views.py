from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from .models import Category
from .forms import CategoryForm

def category_management(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('category_management'))

    categories = Category.objects.all()

    return render(request, 'admin/category.html', {
        'categories': categories,
        'form': form
    })

def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_management')  # Redirect to category management page after update
    else:
        form = CategoryForm(instance=category)
    return render(request, 'admin/edit_category.html', {'form': form})
