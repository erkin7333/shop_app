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
                               validators=[MinLengthValidator(3), MaxLengthValidator(10)])
    confirm = forms.CharField(max_length=30, widget=forms.PasswordInput, required=True,
                              validators=[MinLengthValidator(3), MaxLengthValidator(10)])



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


# from django.contrib.auth.forms import PasswordChangeForm
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'email', 'image']



class ProfileImage(forms.ModelForm):
    class Meta:
        model = User
        fields = ['image']


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'parolga mos kelmaslik': ("Ikkita parol maydoni mos kelmadi."),
    }
    new_password1 = forms.CharField(label=("Yangi Parol"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("Yangi parolni tasdiqlash"),
                                    widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user

class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = dict(SetPasswordForm.error_messages, **{
        "parol_ noto'g'ri": ("Sizning eski parolingiz noto'g'ri kiritilgan. "
                                "Iltimos, uni qayta kiriting."),
    })
    old_password = forms.CharField(label=("Eski parol"),
                                   widget=forms.PasswordInput)