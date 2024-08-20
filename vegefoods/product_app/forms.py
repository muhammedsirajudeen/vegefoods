from django import forms
from product_app.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_name',
            'description',
            'category',
            'price',
            'available_stock',
            'offer',
            'image_1',
            'image_2',
            'image_3'
        ]

        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter product description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter product price'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'available_stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter available stock'}),
            'offer': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter offer details (optional)'}),
            'image_1': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'image_2': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'image_3': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }



