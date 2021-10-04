from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path('profil/', views.profile, name='profil'),
    path('register/', views.UserRegister.as_view(), name="register"),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('change_password/', views.change_password, name='changepassword'),
    path("user_profile/", views.user_objects, name='user_profile'),
    path('order_history/', views.order_history, name='order_history'),

]