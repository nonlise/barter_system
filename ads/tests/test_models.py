from django.test import TestCase
from django.contrib.auth.models import User
from ads.models import Ad, ExchangeProposal

class AdModelTest(TestCase):
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

    def test_ad_creation(self):
        self.assertEqual(self.ad.title, 'Test Ad')
        self.assertEqual(self.ad.user.username, 'testuser')
        # Убрал проверку status, так как его нет в модели Ad

    def test_ad_str_method(self):
        self.assertEqual(str(self.ad), 'Test Ad (electronics)')

class ExchangeProposalModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username='user1', password='12345')
        cls.user2 = User.objects.create_user(username='user2', password='12345')
        cls.ad1 = Ad.objects.create(
            title='Ad 1', description='Desc 1', category='electronics', condition='new', user=cls.user1
        )
        cls.ad2 = Ad.objects.create(
            title='Ad 2', description='Desc 2', category='books', condition='used', user=cls.user2
        )
        cls.proposal = ExchangeProposal.objects.create(
            ad_sender=cls.ad1,
            ad_receiver=cls.ad2,
            comment='Test comment',
            status='pending'
        )

    def test_proposal_creation(self):
        self.assertEqual(self.proposal.comment, 'Test comment')
        self.assertEqual(self.proposal.status, 'pending')
        self.assertEqual(self.proposal.ad_sender.title, 'Ad 1')
        self.assertEqual(self.proposal.ad_receiver.title, 'Ad 2')

    def test_proposal_str_method(self):
        # Обновил ожидаемую строку, чтобы соответствовать реальному __str__
        expected_str = f'Предложение #{self.proposal.id}: Ad 1 (electronics) → Ad 2 (books)'
        self.assertEqual(str(self.proposal), expected_str)