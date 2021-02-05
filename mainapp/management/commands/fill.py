import json
import os

from authapp.models import ShopUser
from django.core.management import BaseCommand
from mainapp.models import ProductCategory, Product

JSON_PATH = 'mainapp/json'

def load_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), encoding="utf-8") as file_json:
        return json.load(file_json)


class Command(BaseCommand):

    def handle(self, *args, **options):
        categories = load_json('categories')
        ProductCategory.objects.all().delete()
        for new_cat in categories:
            obj_cat = ProductCategory.objects.create(**new_cat)
        print('Categories load success')

        products = load_json('products')
        Product.objects.all().delete()
        for new_prod in products:
            cat_name = new_prod['category']
            cur_cat = ProductCategory.objects.get(name=cat_name)
            new_prod['category'] = cur_cat

            obj_prod = Product(**new_prod)
            obj_prod.save()
        print('Products load success')

        ShopUser.objects.create_superuser('django', 'gb@local', 'geekbrains', age='30')
        print('superuser created')
