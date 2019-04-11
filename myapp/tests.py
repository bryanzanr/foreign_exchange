from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse
from importlib import import_module
from rest_framework import status
from rest_framework.test import APIClient
from .forms import CurrencyForm
from .models import Currency, Exchange

# Test-Driven Development (TDD) for Models

class CurrencyTestCase(TestCase):
    def setUp(self):
        self.currency_from = 'USD'
        self.currency_to = 'GBP'
        self.currency = Currency(currency_from=self.currency_from,
                               currency_to=self.currency_to)

    def test_model_can_create_currency(self):
        old_count = Currency.objects.count()
        self.currency.save()
        new_count = Currency.objects.count()
        self.assertNotEqual(old_count, new_count)

class ExchangeTestCase(TestCase):
    def setUp(self):
        self.currency_from = 'USD'
        self.currency_to = 'GBP'
        self.currency = Currency(currency_from=self.currency_from,
                               currency_to=self.currency_to)
        self.currency.save()
        self.exchange_date = '2018-07-01'
        self.currency_id = self.currency.id
        self.exchange_rate = '0.75709'
        self.exchange = Exchange(exchange_date=self.exchange_date,
        exchange_rate=self.exchange_rate, currency_id=self.currency_id)

    def test_model_can_create_exchange(self):
        old_count = Exchange.objects.count()
        self.exchange.save()
        new_count = Exchange.objects.count()
        self.assertNotEqual(old_count, new_count)

# Specs for Request & Response (Validation Testing)

class TestSession(object):

    client = Client()

    def create_session(self):
        session_engine = import_module(settings.SESSION_ENGINE)
        store = session_engine.SessionStore()
        store.save()
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key

class CurrencyFormTest(TestCase):

    def test_valid_data(self):
        form = CurrencyForm({
            'currency_from': 'USD',
            'currency_to': 'GBP'
        })
        self.assertTrue(form.is_valid())
        log = form.save()
        self.assertEqual(log.currency_from, 'USD')
        self.assertEqual(log.currency_to, 'GBP')

    def test_blank_data(self):
        form = CurrencyForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'currency_from': ['This field is required.'],
            'currency_to': ['This field is required.']
        })

    def test_form_validation_for_blank_items(self):
        form = CurrencyForm(data={'currency_from': '', 'currency_to': ''})
        self.assertFalse(form.is_valid())


# Uniform Resource Locator (URL) Testing

class UrlTest(TestSession, TestCase):

    def test_myapp_url_is_exist(self):
        response = Client().get('/api/')
        self.assertEqual(response.status_code, 200)

    def test_currency_url_is_exist(self):
        response = self.client.get('/api/currency/')
        self.assertEqual(response.status_code, 200)

    def test_exchange_url_is_exist(self):
        response = self.client.get('/api/exchange/')
        self.assertEqual(response.status_code, 200)

    def test_form_url_is_exist(self):
        response = self.client.get('/api/date/')
        self.assertEqual(response.status_code, 200)

    def test_list_url_is_exist(self):
        self.create_session()
        session = self.client.session
        session['exchange_date'] = '2018-07-02'
        session.save()
        response = self.client.get('/api/list/')
        self.assertEqual(response.status_code, 200)

    def test_form_page_is_completed(self):
        response = self.client.get('/api/date/')
        self.assertTemplateUsed(response, 'exchange_form.html')

    def test_list_page_is_completed(self):
        self.create_session()
        session = self.client.session
        session['exchange_date'] = '2018-07-02'
        session.save()
        response = self.client.get('/api/list/')
        self.assertTemplateUsed(response, 'exchange_list.html')

# Unit-test for Views (Functional Testing)

class ViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.exchange_date = {
            'exchange_date': '2018-07-02'
        }
        self.response = self.client.post(
            reverse('exchange_form'),
            self.exchange_date,
            format='json'
        )

    def test_api_can_submit_date_to_be_searched(self):
        self.assertEqual(self.response.status_code, status.HTTP_302_FOUND)

    def test_api_can_show_list_of_exchange_rates(self):
        response = self.client.get(
            reverse('exchange_list'),
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
