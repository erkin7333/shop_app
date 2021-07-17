from django.urls import path
from .views import *

app_name = 'shop_product'

urlpatterns = [
    path('', ProductView.as_view(), name='pro'),
    path('page_product/<int:id>/', ProView.as_view(), name='page_product'),
    path('cart/', cart, name='cart'),
    path('add_cart/<int:id>/', add_cart, name='add_cart'),
    path('delete/<int:pk>/', cart_delete, name='delete'),
    path('adres/', adress, name='adress'),
    path('save_adress/', adress_save, name='save_adress'),
]
