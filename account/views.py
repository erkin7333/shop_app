from shop_product.models import Product
from shop_product.views import product_all
from django.db.models import query
from shop_product.forms import SearchForms
from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import RegisterForm, Login_User, ProfileForm, ProfileImage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib import messages
User = get_user_model()
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from shop_product.models import Order

class UserRegister(View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

    def get(self, request):
        form = RegisterForm()
        context = {
            "form": form
        }
        return render(request, 'account/register.html', context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            del data['confirm']
            user = User(**data)
            user.password = make_password(data['password'])
            user.save()
            messages.info(request, "Registratsiyadan ottingiz tizimga kirish uchun 'Tizimga kirishni' bosing ")
            return redirect('account:login')
        
        return render(request, 'account/register.html', {"form": form})


def user_login(request):
    form = Login_User()
    if request.method == 'POST':
        form = Login_User(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.info(request, "Royhatdan otdingiz.")
                return redirect('shop_product:pro')
            form.add_error('password', "Username va/yoki parol noto'g'ri. ")
        
    return render(request, 'account/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, "Tizimdan chiqdinggiz.")
    return redirect('shop_product:pro')

def user_objects(request):
    user_profile = User.objects.get(id=request.user.id)
    context = {
        "user_profile": user_profile
    }
    return render(request, 'account/profile.html', context)

def profile(request):
    prof = User.objects.get(id=request.user.id)
    form_u = ProfileForm(instance=prof)
    if request.method == 'POST':
        form_u = ProfileForm(request.POST, request.FILES, instance=prof)
        if form_u.is_valid():
            form_u.save()
            return redirect("account:profil")
    context = {
        'form_u': form_u,
    
    }
    
        
    return render(request, 'account/profil.html', context)



def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Parolingiz muvaffaqiyatli yangilandi!')
            return redirect('account:profil')
        else:
            messages.error(request, 'Iltimos, pastdagi xatoni tuzating.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/change_password.html', {
        'form': form
    })

def order_history(request):
    user = request.user
    if user.is_authenticated and user.is_superuser:
        orders = Order.objects.all()
        context = {
            "orders": orders
        }
        return render(request, 'account/order_h.html', context)
    return render(request, 'account/order_h.html')