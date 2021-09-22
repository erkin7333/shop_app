from django import forms
from django.db.models import query
from .models import ShippingAddress, Product, Order

# class ChekoutForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['first_name', 'last_name', 'phone', 'email', 'subtotal', 'dicount','total', 'order_status']

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['first_name', "last_name", 'city', 'district', 'street', 'phone', 'email', 'house_number']
class AddProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class SearchForms(forms.Form):
    query = forms.CharField(max_length=100)
    catid = forms.IntegerField()