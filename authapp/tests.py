from django.test import TestCase, Client
from authapp.models import ShopUser


class UserTestCase(TestCase):
    def setUp(self):
        self.username = 'django10'
        self.password = 'geekbrains'
        self.client = Client()
        self.user = ShopUser.objects.create_superuser(
            username=self.username,
            email='django10@dnago10.ru',
            password=self.password
        )

    def test_user_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.content['user'].is_anonymous)
        self.assertEqual(response.content['title'], 'Главная')
        self.assertNotContains(response, 'Администрирование')

        self.client.login(username=self.username, password=self.password)

        response = self.client.get('/auth/login/')
        self.assertFalse(response.content['user'].is_anonymous)
        self.assertEqual(response.content['user'], self.user)

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content['title'], 'Главная')
        self.assertContains(response, 'Администрирование')

