# Generated by Django 3.2.5 on 2021-10-11 15:59

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uz', models.CharField(blank=True, max_length=200, null=True)),
                ('name_ru', models.CharField(blank=True, max_length=200, null=True)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='shop_product/')),
                ('description', models.TextField()),
                ('rating', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('numReviews', models.IntegerField(blank=True, default=0, null=True)),
                ('marked_price', models.PositiveIntegerField()),
                ('selling_price', models.PositiveIntegerField()),
                ('warranty', models.CharField(blank=True, max_length=250, null=True)),
                ('return_policy', models.CharField(blank=True, max_length=250, null=True)),
                ('view_count', models.PositiveIntegerField(default=0)),
                ('countInstok', models.IntegerField(blank=True, default=0, null=True)),
                ('createDat', models.DateTimeField(auto_now_add=True)),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop_product.brand')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop_product.category')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('rating', models.IntegerField(blank=True, default=0, null=True)),
                ('comment', models.TextField()),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop_product.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payme',
            fields=[
                ('carta_numbr', models.CharField(max_length=16, primary_key=True, serialize=False, validators=[django.core.validators.MinLengthValidator(16), django.core.validators.MaxLengthValidator(17), django.core.validators.RegexValidator('^\\d{1,16}$')], verbose_name='Karta nomeri')),
                ('carta_data', models.IntegerField(max_length=5, verbose_name='Karta mudati')),
                ('cart', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop_product.cart')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=250, null=True)),
                ('last_name', models.CharField(blank=True, max_length=250, null=True)),
                ('city', models.CharField(blank=True, max_length=200, null=True, verbose_name='Shahar / Viloyat')),
                ('district', models.CharField(blank=True, max_length=200, null=True, verbose_name='Tuman')),
                ('street', models.CharField(blank=True, max_length=200, null=True, verbose_name="Ko'cha")),
                ('house_number', models.IntegerField(blank=True, max_length=14, null=True, verbose_name='Uy nomeri')),
                ('phone', models.CharField(max_length=14, verbose_name='Telefon Nomer')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Elektron Pochta')),
                ('discount', models.PositiveIntegerField()),
                ('subtotal', models.PositiveIntegerField()),
                ('total', models.PositiveIntegerField()),
                ('order_status', models.CharField(choices=[('Buyurtma qabul qilindi', 'Buyurtma qabul qilindi'), ('Buyurtmani qayta ishlash', 'Buyurtmani qayta ishlash'), ("Yo'lda", "Yo'lda"), ('Buyurtma bajarildi', 'Buyurtma bajarildi'), ('Buyurtma bekor qilindi', 'Buyurtma bekor qilindi')], default=1, max_length=250)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('cart', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop_product.cart')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.PositiveIntegerField()),
                ('quantity', models.PositiveIntegerField()),
                ('subtotal', models.PositiveIntegerField()),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop_product.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop_product.product')),
            ],
        ),
        migrations.AddField(
            model_name='brand',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop_product.category'),
        ),
    ]
