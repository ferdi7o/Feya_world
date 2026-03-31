from django import forms
from .models import Product, Review, ProductVariant

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
        if rating and (rating < 1 or rating > 10):
            raise forms.ValidationError("Моля, въведете оценка между 1 и 10.")
        return rating

class ProductForm(forms.ModelForm):
    images = forms.ImageField(
        label="Снимки (изберете няколко)",
        required=False,
        help_text="Можете да изберете няколко снимки наведнъж."
    )

    class Meta:
        model = Product
        fields = ['title', 'category', 'description', 'price', 'product_type', 'is_shipping_free', 'shipping_cost']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Име на продукта...'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'product_type': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['images'].widget.attrs.update({'multiple': True, 'class': 'form-control'})

class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['size', 'stock']
        widgets = {
            'size': forms.TextInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }