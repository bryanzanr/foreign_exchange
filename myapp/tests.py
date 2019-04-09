from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
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
        self.currency_id = self.currency
        self.exchange_rate = '0.75709'
        self.exchange = Exchange(exchange_date=self.exchange_date,
        exchange_rate=self.exchange_rate, currency_id=self.currency_id)

    def test_model_can_create_exchange(self):
        old_count = Exchange.objects.count()
        self.exchange.save()
        new_count = Exchange.objects.count()
        self.assertNotEqual(old_count, new_count)

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
