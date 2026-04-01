from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'address', 'city', 'phone']
        labels = {
            'first_name': 'Име',
            'last_name': 'Фамилия',
            'phone': "Телефонен номер",
            'address': 'Адрес за доставка',
            'city': 'Град',
        }


class OrderDeleteForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        label="Потвърждавам, че искам да изтрия тази поръчка",
        help_text="Това действие е необратимо!"
    )