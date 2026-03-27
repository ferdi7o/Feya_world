
from .models import Review
from django import forms
from .models import Product, ProductVariant

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'content']
        labels = {
            'rating': 'Вашата оценка (1-10)',
            'content': 'Вашият коментар',
        }
        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
                'placeholder': 'Оценка от 1 до 10'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Напишете вашето мнение тук...'
            }),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 10:
            raise forms.ValidationError("Моля, въведете оценка между 1 и 10.")
        return rating

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # Bazı alanları hariç tutuyoruz (Exclude requirement)
        exclude = ['created_at', 'updated_at']
        labels = {
            'title': 'Име на продукта',
            'price': 'Цена (лв)',
            'product_type': 'Тип на продукта',
        }

class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = '__all__'
        widgets = {
            # Ödevdeki "Read-only veya Disabled field" gereksinimi
            'product': forms.Select(attrs={'readonly': 'readonly', 'class': 'form-control-plaintext'}),
        }