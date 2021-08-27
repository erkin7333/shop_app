from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View, UpdateView, DetailView
from .models import Product, Cart, Order, OrderItem
from django.db.models import F, Sum, Avg
from .forms import AdressForm, AddProduct
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist



class ProductView(ListView):
    model = Product
    template_name = "shop_product/product.html"
    context_object_name = 'products'
    paginate_by = 4




class ItemDetailView(DetailView):
    model = Product
    template_name = "shop_product/produc_page.html"

@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(product__slug=product.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("shop_product:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("shop_product:order-summary")
    else:
        order = Order.objects.create(
            user=request.user,)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("shop_product:order-summary")


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'shop_product/cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


@login_required
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(product__slug=product.slug).exists():
            order_item = OrderItem.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("shop_product:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)



@login_required
def remove_single_item_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(product__slug=product.slug).exists():
            order_item = OrderItem.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("shop_product:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("shop_product:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("shop_product:product", slug=slug)



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


def add_cart(request):
    pass