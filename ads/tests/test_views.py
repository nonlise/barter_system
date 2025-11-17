from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ads.models import Ad, ExchangeProposal

class AdViewsTest(TestCase):
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
        cls.client = Client()

    def test_ad_list_view(self):
        response = self.client.get(reverse('ads:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Ad')
        self.assertTemplateUsed(response, 'ads/list.html')

    def test_ad_detail_view(self):
        response = self.client.get(reverse('ads:detail', args=[self.ad.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Description')
        self.assertTemplateUsed(response, 'ads/detail.html')

    def test_ad_create_view_authenticated(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('ads:create'), {
            'title': 'New Ad',
            'description': 'New Description',
            'category': 'books',
            'condition': 'used'
        })
        self.assertEqual(response.status_code, 302)  # Редирект после успешного создания
        self.assertEqual(Ad.objects.count(), 2)

    def test_ad_create_view_unauthenticated(self):
        response = self.client.get(reverse('ads:create'))
        self.assertEqual(response.status_code, 302)  # Редирект на login page
        self.assertRedirects(response, '/accounts/login/?next=/create/')