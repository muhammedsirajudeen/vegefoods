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

    def clean_category_name(self):
        category_name = self.cleaned_data.get('category_name')
        if Category.objects.filter(category_name__iexact= category_name):
            raise forms.ValidationError('Category name already exists')
        
        if not category_name.isalpha():
            raise forms.ValidationError('Category name must contain Character')
        return category_name
    
    def clean_category_unit(self):
        category_unit = self.cleaned_data.get('category_unit')
        if not category_unit.isalpha():
            raise forms.ValidationError('Category unit must contain Character')
        return category_unit

    def clean(self):
        cleaned_data = super().clean()
        category_name = cleaned_data.get('category_name')
        category_unit = cleaned_data.get('category_unit')

       
        if category_name:
            cleaned_data['category_name'] = category_name.title()

        if category_unit:
            cleaned_data['category_unit'] = category_unit.lower()
        return cleaned_data