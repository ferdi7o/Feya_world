from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Моля, въведете валиден имейл адрес.")

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'avatar']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Адрес за доставка...'}),
        }