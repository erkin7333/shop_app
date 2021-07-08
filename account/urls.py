from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path('', views.index, name='index'),
    path('profil/', views.profile, name='profil'),
    path('register/', views.UserRegister.as_view(), name="register"),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]