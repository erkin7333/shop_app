from django import forms
from shop_settings.validators import PhoneValidator
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from .models import User


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, required=True,
                               validators=[UnicodeUsernameValidator()])
    phone = forms.CharField(max_length=14, required=True,
                            validators=[PhoneValidator()])
    password = forms.CharField(max_length=30, widget=forms.PasswordInput, required=True,
                               validators=[MinLengthValidator(3), MaxLengthValidator(6)])
    confirm = forms.CharField(max_length=30, widget=forms.PasswordInput, required=True,
                              validators=[MinLengthValidator(3), MaxLengthValidator(6)])



    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data.get('username')).exists():
            raise ValidationError("Ushbu foydalanuvchi nomi bilan ro'yxatdan o'tilgan")
        return self.cleaned_data['username']

    def clean_phone(self):
        if User.objects.filter(phone=self.cleaned_data.get('phone')).exists():
            raise ValidationError("Ushbu telefon raqam bilan ro'yxatdan o'tilgan")
        return self.cleaned_data['phone']

    def clean_confirm(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm']:
            raise ValidationError("Parollar bir xil emas ")
        return self.cleaned_data['confirm']




class Login_User(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)



class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'email', 'password', 'image']



class ProfileImage(forms.ModelForm):
    class Meta:
        model = User
        fields = ['image']