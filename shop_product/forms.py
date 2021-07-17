from django import forms
from .models import ShoppingAddress



class AdressForm(forms.ModelForm):
    class Meta:
        model = ShoppingAddress
        fields = '__all__'
