from django import template
from shop_product.models import Product

register = template.Library()


@register.simple_tag()
def filter_category(category):
    return Product.objects.filter(category=category)