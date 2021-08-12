from django import forms
from .models import ShoppingAddress, Product



class AdressForm(forms.ModelForm):
    class Meta:
        model = ShoppingAddress
        fields = '__all__'


class AddProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'