import datetime

from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from mainapp.models import Product, ProductCategory
import random, os, json

JSON_PATH = 'mainapp/json'


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products_by_category(pk):
    if settings.LOW_CACHE:
        key = f'products_by_category{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True, category__pk=pk)
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True, category__pk=pk)


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), encoding="utf-8") as infile:
        return json.load(infile)


def get_hot_product():
    products_list = Product.objects.filter(category__is_active=True)
    return random.sample(list(products_list), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products


def main(request):
    title = 'Главная'
    products = Product.objects.filter(category__is_active=True).select_related()[:3]
    content = {'title': title, 'products': products}
    return render(request, 'mainapp/index.html', content)


def product(request, pk):
    title = 'Товар'
    product_item = get_object_or_404(Product, pk=pk)
    # links_menu = ProductCategory.objects.filter(is_active=True)
    content = {'title': title,
               'product': product_item,
               # 'links_menu': links_menu
               'links_menu': get_links_menu()
               }
    return render(request, 'mainapp/product.html', content)


@cache_page(3600)
def products(request, pk=None, page=1):
    title = 'Товары'
    # links_menu = ProductCategory.objects.filter(is_active=True)

    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all()
            # products_list = Product.objects.filter(Q(category_id=5) | Q(category_id=1))
            category = {'pk': 0, 'name': 'Все товары'}
        else:
            category = get_category(pk)
            products_list = Product.objects.filter(category__pk=pk)
            current_category = ProductCategory.objects.get(pk=pk)
            title = current_category.name

        # if 'page' in request.GET:
        #     page = request.GET.get('page')
        #     paginator = Paginator(products_list, 2)
        #     try:
        #         product_paginator = paginator.page(page)
        #     except PageNotAnInteger:
        #         product_paginator = paginator.page(1)
        #     except EmptyPage:
        #         product_paginator = paginator.page(paginator.num_pages)
        #     content['products'] = product_paginator

        paginator = Paginator(products_list, 2)
        try:
            product_paginator = paginator.page(page)
        except PageNotAnInteger:
            product_paginator = paginator.page(1)
        except EmptyPage:
            product_paginator = paginator.page(paginator.num_pages)
        content = {
            'title': title,
            # 'links_menu': links_menu,
            'links_menu': get_links_menu(),
            'category': category,
            'products': product_paginator
        }
        return render(request, 'mainapp/products_list.html', content)
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    content = {'title': title,
               # 'links_menu': links_menu,
               'links_menu': get_links_menu(),
               'same_products': same_products,
               'hot_product': hot_product
               }
    return render(request, 'mainapp/products.html', content)


def contacts(request):
    title = 'О нас'
    visit_date = datetime.datetime.now()
    locations = load_from_json('contacts')
    content = {
        'title': title,
        'visit_date': visit_date,
        'locations': locations
    }
    return render(request, 'mainapp/contacts.html', content)
