from django.test import TestCase, Client

from mainapp.models import Product, ProductCategory


class MainAppTestCase(TestCase):
    EXPECTED_STATUS_CODE = 200

    def setUp(self):
        self.client = Client()
        category = ProductCategory.objects.create(
            name='test_cat'
        )
        for i in range(20):
            Product.objects.create(
                name=f'test_prod_{i}',
                category=category
            )

    def test_mainpage_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.EXPECTED_STATUS_CODE)

        for product in Product.objects.all():
            response = self.client.get(f'/products/product/{product.pk}')
            self.assertEqual(response.status_code, self.EXPECTED_STATUS_CODE)
