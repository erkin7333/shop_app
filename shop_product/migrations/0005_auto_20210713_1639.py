# Generated by Django 3.2.5 on 2021-07-13 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_product', '0004_auto_20210712_1143'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='brnad',
            new_name='brand',
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='shop_product/'),
        ),
    ]
