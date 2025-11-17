from django.test import TestCase
from ads.forms import AdForm, SignUpForm, ExchangeProposalForm
from django.contrib.auth.models import User
from ads.models import Ad

class AdFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'title': 'Test Ad',
            'description': 'Test Description',
            'category': 'electronics',
            'condition': 'new',
            'image_url': 'http://example.com/image.jpg'
        }
        form = AdForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {'title': '', 'description': 'Test'}  # title обязательно
        form = AdForm(data=form_data)
        self.assertFalse(form.is_valid())

class SignUpFormTest(TestCase):
    def test_valid_signup(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_password_mismatch(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'password1',
            'password2': 'password2'
        }
        form = SignUpForm(data=form_data)
        # Исправлено: форма должна быть невалидной при несовпадении паролей
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

class ExchangeProposalFormTest(TestCase):
    def test_valid_proposal_form(self):
        form_data = {'comment': 'I want to exchange!'}
        form = ExchangeProposalForm(data=form_data)
        self.assertTrue(form.is_valid())