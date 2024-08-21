from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'category_name',
            'category_image',
            'category_offer',
       
            'category_unit'
        ]
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'}),
            'category_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'category_offer': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter category offer', 'step': '0.01'}),
            'category_unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter unit (e.g., kg, packet)'}),
        }
