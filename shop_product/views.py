from django.shortcuts import render, redirect
from django.views.generic import ListView, View
from .models import Product, Cart
from django.db.models import F, Sum, Avg
from .forms import AdressForm, AddProduct
from django.core.paginator import Paginator
class ProductView(ListView):
    model = Product
    template_name = "shop_product/product.html"
    context_object_name = 'products'
    paginate_by = 4

# def products(request):
#     queryset = Product.objects.all()
#     paginator = Paginator(queryset, 8) # Show 25 contacts per page.
#
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'shop_product/product.html', {'page_obj':page_obj})
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
        cart_sum = Cart.objects.filter(user=request.user).aggregate(Sum("product__price"))
    else:
        cart_sum = Cart.objects.filter(user=request.user).aggregate(Sum("product__price"))
        carts = Cart.objects.filter(user=request.user)
    context = {
        'carts': carts,
    }
    context['cart_sum'] = cart_sum['product__price__sum']
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



def adress(request):
    qwerty = AdressForm()
    context = {
        'qwerty': qwerty
    }
    return render(request, 'shop_product/adress.html', context)


def adress_save(request):
    if request.method == 'POST':
        form = AdressForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("shop_product:save_adress")
        return render(request, 'shop_product/adress.html')


def add_product(request):
    form = AddProduct()
    context = {
        'form': form
    }
    return render(request, "shop_product/add_product.html", context)


# def addproduct(request):
#     if request.method == 'POST':
#         form = AddProduct()
#         context = {
#             'form': form
#         }
#         return render(request, 'shop_product/add_product.html', context)


#
# def pro_category(request):
#     products = Product.objects.filter(brand__icontains='Apple')
#
#     return render(request, 'shop_product/categorya.html', {"products":products})
#
