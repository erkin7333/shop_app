from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from decimal import *

User = get_user_model()
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.db.models import Sum


class Category(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='shop_product/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField()
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    numReviews = models.IntegerField(default=0, null=True, blank=True)
    price = models.FloatField()
    countInstok = models.IntegerField(default=0, blank=True, null=True)
    createDat = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()
    discount_price = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.image.closed:
            img = Image.open(self.image)
            img.thumbnail((500, 500), Image.ANTIALIAS)

            tmp = BytesIO()
            img.save(tmp, 'PNG')
            self.image = File(tmp, 'image.png')
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("shop_product:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("shop_product:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("shop_product:remove-from-cart", kwargs={
            'slug': self.slug
        })

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    rating = models.IntegerField(default=0, blank=True, null=True)
    comment = models.TextField()

    def __str__(self):
        return str(self.rating)


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    image = models.CharField(max_length=255, blank=True, null=True)
    ordered = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_item_price(self):
        return self.quantity * self.product.price

    def get_total_discount_item_price(self):
        return self.quantity * self.product.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    items = models.ManyToManyField(OrderItem)
    paymentMethod = models.CharField(max_length=200, blank=True, null=True)
    taxPrice = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    shoppingPrice = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    totalPrice = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    isDelivered = models.BooleanField(default=False)
    deliveredAt = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return str(self.createdAt)


    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


class ShoppingAddress(models.Model):
    # order = models.OneToOneField(Order, on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    postalCode = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    shoppingPrice = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.address


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    qty = models.IntegerField(null=True, blank=True)
