from django import template
from shop_product.models import CartProduct, Product, Cart

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Cart.objects.filter(user=user)
        to = CartProduct.objects.all()
        
    return 0

