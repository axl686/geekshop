# Generated by Django 3.1 on 2020-08-25 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_product_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='products_images/default.jpg', upload_to='products_images'),
        ),
    ]
