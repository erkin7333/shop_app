from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import RegisterForm, Login_User, ProfileForm, ProfileImage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
User = get_user_model()



def index(request):
    return render(request, 'layout.html')


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
                return redirect('account:index')
            form.add_error('password', "Username va/yoki parol noto'g'ri. ")

    return render(request, 'account/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('account:index')



def profile(request):
    prof = User.objects.get(id=request.user.id)
    form_u = ProfileForm(instance=prof)
    if request.method == 'POST':
        form_u = ProfileForm(request.POST, request.FILES, instance=prof)
        if form_u.is_valid():
            # request.POST['password'] = make_password(request.POST['password'])
            form_u.save()
            # done.password = make_password(request.POST.get('password'))
            return redirect("account:profil")
    context = {
        'form_u': form_u,
    }
    return render(request, 'account/profil.html', context)