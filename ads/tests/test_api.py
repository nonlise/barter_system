from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from ads.models import Ad

class AdAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.ad = Ad.objects.create(
            title='Test Ad',
            description='Test Description',
            category='electronics',
            condition='new',
            user=cls.user
        )

    def test_get_ads_list(self):
        # Добавил аутентификацию, так как API требует авторизации
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/ads/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_ad_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Ad',
            'description': 'New Description',
            'category': 'books',
            'condition': 'used',
            'user': self.user.id  # Добавил обязательное поле user
        }
        response = self.client.post('/api/ads/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ad.objects.count(), 2)

    def test_create_ad_unauthenticated(self):
        data = {'title': 'New Ad', 'description': 'New Description'}
        response = self.client.post('/api/ads/', data)
        # Изменил ожидаемый код на 403, так как в настройках используется IsAuthenticated
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)