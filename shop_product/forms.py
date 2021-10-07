from django import forms
from django.db.models import query
from .models import Product, Order, Payme
from django.core.exceptions import ValidationError


# class ChekoutForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['first_name', 'last_name', 'phone', 'email', 'subtotal', 'dicount','total', 'order_status']
#
# class ShippingAddressForm(forms.ModelForm):
#     class Meta:
#         model = ShippingAddress
#         fields = ['first_name', "last_name", 'city', 'district', 'street', 'phone', 'email', 'house_number']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'city', 'district', 'street', 'house_number', 'order_status']

class PaymeForm(forms.ModelForm):
    class Meta:
        model = Payme
        fields = ['carta_numbr', 'carta_data']
        

class AddProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'cols': 21}),
        }


class SearchForms(forms.Form):
    query = forms.CharField(max_length=100)
    catid = forms.IntegerField()

