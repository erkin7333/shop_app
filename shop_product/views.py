from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, View, UpdateView, DetailView, TemplateView
from django.views.generic.edit import CreateView
from django.views.generic import ListView, View, UpdateView, DetailView, CreateView, TemplateView, DeleteView
from .models import Product, Cart, Order, Brand, Category, CartProduct
from .forms import AddProduct, SearchForms, OrderForm, PaymeForm
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class ProductView(ListView):
    model = Product
    template_name = "shop_product/product.html"
    context_object_name = 'products'
    paginate_by = 4


class TopProducts(ListView):
    model = Product
    template_name = "shop_product/top_products.html"
    context_object_name = 'products'
    paginate_by = 4


class ProductDetailView(LoginRequiredMixin, TemplateView):
    template_name = "shop_product/produc_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        prod = Product.objects.get(slug=url_slug)
        prod.view_count += 1
        prod.save()
        context['product'] = prod
        return context


class UserOrderDetaile(DetailView):
    template_name = 'shop_product/order_detail.html'
    model = Order
    context_object_name = "ord_obj"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pass
        else:
            return redirect('account:login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserOrderDetaile, self).get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context


class AddToCartView(LoginRequiredMixin, View):
    def get(self, request, pro_id):
        product_id = pro_id
        # mahsulotni olish

        product_obj = Product.objects.get(id=product_id)
        #     # Maxsulot mavjudligini tekshirish
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(product=product_obj)
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.selling_price
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
            else:
                cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj,
                                                         rate=product_obj.selling_price,
                                                         quantity=1, subtotal=product_obj.selling_price)

                cart_obj.total += product_obj.selling_price
                cart_obj.save()
        else:
            cart_obj = Cart.objects.create(user=self.request.user, total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj,
                                                     rate=product_obj.selling_price, subtotal=product_obj.selling_price,
                                                     quantity=1)
            cart_obj.total += product_obj.selling_price
            cart_obj.save()

        messages.info(request, "Bu mahsulot savatga qo'shildi.")
        return redirect('shop_product:mycart')


class MyCartView(TemplateView):
    template_name = "shop_product/cart.html"

    def get_context_data(self, **kwargs):
        context = super(MyCartView, self).get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cartt = Cart.objects.get(id=cart_id)
        else:
            cartt = None
        context['cartt'] = cartt
        return context


class AllDeleteView(View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
            messages.info(request, "Bu narsalar savatchangizdan tozalandi.")
        return redirect('shop_product:mycart')


class ChekoutView(CreateView):
    template_name = 'shop_product/chekout.html'
    form_class = OrderForm
    success_url = reverse_lazy("shop_product:myorder")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            user = self.request.user
            form.instance.user = user
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.order_status = "Buyurtma qabul qilindi"
            del self.request.session['cart_id']
        else:
            return redirect('shop_product:myorder')
        return super().form_valid(form)


class PaymeViews(CreateView):
    template_name = "shop_product/to'lov.html"
    form_class = PaymeForm
    success_url = reverse_lazy("shop_product:pro")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get("cart_id")
        else:
            cart_obj = None
        context['payme'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            user = self.request.user
            form.instance.user = user
            form.instance.cart = cart_obj
            form.instance.total = cart_obj.total
            del self.request.session['cart_id']
        else:
            return redirect('shop_product:pro')
        return super().form_valid(form)


def orderview(request):
    users = request.user
    orders = Order.objects.filter(user=users)
    context = {
        "orders": orders
    }
    return render(request, 'shop_product/order.html', context)


class ManagerCartView(View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs['cp_id']
        action = request.GET.get('action')
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart
        if action == "inc":
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            messages.info(request, "Bu mahsulot miqdori yangilandi.")
            cart_obj.save()
        elif action == "dcr":
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            messages.info(request, "Bu mahsulot savatdan olib tashlandi.")
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()
        elif action == "rmv":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
            messages.info(request, "Bu element savatchadan o???chirib tashlandi.")
        return redirect('shop_product:mycart')


class ProductFilter(ListView):
    model = Product

    # context_object_name = 'filter_pro'
    def get_queryset(self):
        result = super(ProductFilter, self).get_queryset()
        category_filter = self.request.GET.get('category')
        if category_filter:
            result = Product.objects.filter(Q(category__icontains=category_filter))
        return result


def add_product(request):
    form = AddProduct()
    context = {
        'form': form
    }
    return render(request, "shop_product/add_product.html", context)


class ProductEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    template_name = "shop_product/product_edit.html"
    success_url = "/"
    fields = '__all__'

    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_superuser or obj.user == self.request.user


def useraddproduct(request):
    if request.method == 'POST':
        form = AddProduct(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = AddProduct()
        user = request.user
        user_all_pro = Product.objects.filter(user=user)
        context = {
            'user_all_pro': user_all_pro,
            'form': form
        }
    return render(request, "shop_product/add_product.html", context)


def category_by_id(request, pk):
    print(pk)
    category_f = Product.objects.filter(category_id=pk)
    brand_all = Brand.objects.filter(category=pk)
    context = {
        'category_f': category_f,
        'brand_all': brand_all,
    }
    return render(request, 'shop_product/categorya.html', context)


def product_all(request):
    cat = Category.objects.all()
    all_product = Product.objects.all()
    context = {
        'cat': cat,
        "all_product": all_product,
    }
    return render(request, 'shop_product/all_category.html', context)


def brand_by_id(request, pk):
    brand_f = Product.objects.filter(brand_id=pk)

    context = {
        'brand_f': brand_f,

    }
    return render(request, "shop_product/brand.html", context)


"""
<< Delete product >>
"""
def delete_product(request, id):
    products = Product.objects.get(pk=id)
    products.delete()
    messages.info(request, "Product ochirildi.")
    return redirect('shop_product:pro')


"""
<< Search product >>
"""
def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        products = Product.objects.filter(name_uz__icontains=searched)
        context = {
            'searched': searched,
            'products': products,
        }

        return render(request, "shop_product/search.html", context)
    else:
        return render(request, "shop_product/search.html")


"""
<< Search product in category_page >>
"""


def search_cat(request):
    if request.method == "POST":
        searched_cat = request.POST['searched_cat']
        all_product = Product.objects.filter(name__icontains=searched_cat)
        context = {
            'searched_cat': searched_cat,
            'all_product': all_product,
        }

        return render(request, "shop_product/all_category.html", context)
    else:
        return render(request, "shop_product/all_category.html")
