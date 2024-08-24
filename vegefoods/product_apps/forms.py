from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_name',
            'description',
            'category',
            'available_stock',
            'price',
            'offer',
            'image_1',
            'image_2',
            'image_3',

        ]
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter product description'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'available_stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter available stock'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter product price', 'step': '0.01'}),
            'offer': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter discount offer', 'step': '0.01'}),
            'image_1': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'image_2': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'required': False}),
            'image_3': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'required': False}),
     
        }

    def clean_product_name(self):
        product_name =  self.cleaned_data.get('product_name')
        if Product.objects.filter(product_name__iexact=product_name).exists():
            raise forms.ValidationError('A product with this name already exists.')
        return product_name.title()
    
    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        if len(description) < 250:
            raise forms.ValidationError('Description must be at least 250 characters long.')
        return description
        
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError('Price must be a positive number.')
        return price


    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        available_stock = cleaned_data.get("available_stock")
        
        if category and available_stock is not None:
            if available_stock < 0:
                self.add_error('available_stock', 'Stock must be a positive number.')

        return cleaned_data
