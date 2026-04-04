from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Моля, въведете валиден имейл адрес.")

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(label="Имейл адрес (не може да се променя)")

    class Meta:
        model = Profile
        fields = ['avatar', 'phone', 'address', 'email']
        labels = {
            'avatar': 'Профилна снимка',
            'phone': 'Телефонен номер',
            'address': 'Адрес',
        }
        widgets = {
            'phone': forms.TextInput(attrs={'rows': 2, 'placeholder': '+359...'}),
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Адрес за доставка...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].disabled = True
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})