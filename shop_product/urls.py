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
    path('add_pro/', add_product, name='add_pro'),
    path('product_edit/<int:pk>/', ProductEdit.as_view(), name='product_edit'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('category/<int:pk>/', category_by_id, name='category_by_id'),
    path('brand/<int:pk>/', brand_by_id, name='brand'),
    path('product_all/', product_all, name='all_product')

]
