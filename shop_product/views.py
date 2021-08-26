from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, View, UpdateView
from .models import Product, Cart, Category, Brand
from django.db.models import F, Sum, Avg
from .forms import AdressForm, AddProduct

from django.db.models import Q
from django.contrib.auth.decorators import login_required



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
    # ordering = ['-added_at']


class ProductFilter(ListView):
    model = Product

    # context_object_name = 'filter_pro'
    def get_queryset(self):
        result = super(ProductFilter, self).get_queryset()
        category_filter = self.request.GET.get('category')
        if category_filter:
            result = Product.objects.filter(Q(category__icontains=category_filter))
        return result


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
    obj = Cart.objects.get(product_id=pk)
    obj.delete()
    return redirect('shop_product:cart')

def all_delete(request):
    obj = Cart.objects.all()
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
def pro_category(request):
    return render(request, 'shop_product/categorya.html', )


class ProductEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    template_name = "shop_product/product_edit.html"
    success_url = "/"
    fields = '__all__'

    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_superuser or obj.user == self.request.user


# def category_filter(request):
#     cat = Category.objects.all()
#     context = {
#         'cat': cat,
#     }
#     return render(request, 'shop_product/categorya.html', context)


def category_by_id(request, pk):
    category_f = Product.objects.filter(category_id=pk)
    brand_all = Brand.objects.all()
    context = {
        'category_f': category_f,
        'brand_all': brand_all,
    }
    return render(request, 'shop_product/categorya.html', context)

def product_all(request,):
    cat = Category.objects.all()
    all_product = Product.objects.all()
    context = {
        'cat': cat,
        "all_product": all_product,
    }
    return render(request, 'shop_product/all_category.html', context)

def brand_by_id(request, pk):
    brand_f = Product.objects.filter(brand_id=pk)
    brand_all = Brand.objects.all()
    context = {
        'brand_f': brand_f,
        'brand_all': brand_all,
    }
    return render(request, "shop_product/brand.html", context)
