from django.shortcuts import render, redirect
from django.views.generic import ListView, View
from .models import Product, Cart


class ProductView(ListView):
    model = Product
    template_name = "shop_product/product.html"
    context_object_name = 'products'


class ProView(View):

    def get(self, request, id, *args, **kwargs):
        product = Product.objects.get(id=id)
        return render(request, "shop_product/produc_page.html", {
            "product": product
        })

def cart(request):
    carts = None
    if request.user.is_superuser:
        carts = Cart.objects.all()
    else:
        carts = Cart.objects.filter(user=request.user)
    context = {
        'carts': carts,
    }
    return render(request, "shop_product/cart.html", context)


def add_cart(request, id):
    product = Product.objects.get(id=id)
    user = request.user
    cart = Cart()
    cart.product = product
    cart.user = user
    done = Cart.objects.filter(user=user, product=product)
    if not done.exists():
        cart.save()
        return redirect('shop_product:cart')
    return redirect('shop_product:cart')


def cart_delete(request, pk):
    obj = Cart.objects.get(pk=pk)
    obj.delete()
    return redirect('shop_product:cart')