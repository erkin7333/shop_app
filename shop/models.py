from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files import File


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    brand = models.CharField(max_length=100)
    rating = models.FloatField()
    views = models.IntegerField()
    images1 = models.ImageField(upload_to='product')
    images2 = models.ImageField(upload_to='product')
    images3 = models.ImageField(upload_to='product')
    images4 = models.ImageField(upload_to='product')

    def save(self, *args, **kwargs):
        if not self.mages1.closed:
            img = Image.open(self.mages1)
            img.thumbnail((500, 500), Image.ANTIALIAS)

            tmp = BytesIO()
            img.save(tmp, 'PNG')
            self.mages1 = File(tmp, 'image.png')
        return super().save(*args, **kwargs)
    def save1(self, *args, **kwargs):
        if not self.images2.closed:
            img = Image.open(self.images2)
            img.thumbnail((500, 500), Image.ANTIALIAS)

            tmp = BytesIO()
            img.save(tmp, 'PNG')
            self.images2 = File(tmp, 'image.png')
        return super().save(*args, **kwargs)
    def save2(self, *args, **kwargs):
        if not self.images3.closed:
            img = Image.open(self.images3)
            img.thumbnail((500, 500), Image.ANTIALIAS)

            tmp = BytesIO()
            img.save(tmp, 'PNG')
            self.images3 = File(tmp, 'image.png')
        return super().save(*args, **kwargs)
    def save3(self, *args, **kwargs):
        if not self.images4.closed:
            img = Image.open(self.images4)
            img.thumbnail((500, 500), Image.ANTIALIAS)

            tmp = BytesIO()
            img.save(tmp, 'PNG')
            self.images4 = File(tmp, 'image.png')
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


