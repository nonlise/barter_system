from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ads.models import Ad

class AdSearchTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        Ad.objects.create(
            title='iPhone 12',
            description='Great condition',
            category='electronics',
            condition='used',
            user=cls.user
        )
        Ad.objects.create(
            title='Python Book',
            description='Learn Python',
            category='books',
            condition='new',
            user=cls.user
        )

    def test_search_by_title(self):
        response = self.client.get(reverse('ads:search') + '?q=iPhone')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'iPhone 12')
        self.assertNotContains(response, 'Python Book')

    def test_search_by_category(self):
        response = self.client.get(reverse('ads:search') + '?category=books')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python Book')
        self.assertNotContains(response, 'iPhone 12')

    def test_search_by_condition(self):
        response = self.client.get(reverse('ads:search') + '?condition=new')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python Book')
        self.assertNotContains(response, 'iPhone 12')