from django.urls import path
from .views import *

app_name = 'shop_product'

urlpatterns = [
    path('', ProductView.as_view(), name='pro'),

    path('product_detail/<slug:slug>/', ProductDetailView.as_view(), name='pro_detail'),

    path('my_cart/', MyCartView.as_view(), name='mycart'),

    path('add-to-cart/<int:pro_id>/', AddToCartView.as_view(), name='add_to_cart'),

    path('manager-cart/<int:cp_id>/', ManagerCartView.as_view(), name='manager'),

    path('all_delete/', AllDeleteView.as_view(), name='alldelete'),

    path('chekout/', ChekoutView.as_view(), name='chekout'),

    path('order/', orderview, name='myorder'),

    path('add_pro/', add_product, name='add_pro'),

    path('useraddpro/', useraddproduct, name='useraddproduct'),

    path('product_edit/<int:pk>/', ProductEdit.as_view(), name='product_edit'),

    path('category/<int:pk>/', category_by_id, name='category_by_id'),

    path('brand/<int:pk>/', brand_by_id, name='brand'),

    path('product_all/', product_all, name='all_product'),

    path('delete/<int:id>/', delete_product, name='delete_product'),

    path('search/', search, name='search'),

    path('search_cat/', search_cat, name='search_cat'),

    path('top_products/', TopProducts.as_view(), name='top_products')

]
