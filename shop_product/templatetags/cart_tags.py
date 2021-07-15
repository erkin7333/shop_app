from django import template
from shop_product.models import Cart

register = template.Library()

@register.filter
def count_cart(user):
    obj = Cart.objects.filter(user=user)
    return obj.count()